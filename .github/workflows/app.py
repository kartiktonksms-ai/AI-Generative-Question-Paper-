from flask import Flask, render_template, redirect, url_for, flash, request, send_file, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_secret_key_change_this')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from extensions import db, login_manager, csrf
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from models import User, QuestionPaper
from forms import LoginForm, RegistrationForm, GeneratePaperForm, SUBJECT_TOPICS
from utils import generate_questions, save_as_pdf


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.email == form.email.data) | (User.username == form.username.data)
        ).first()
        if existing_user:
            flash('An account with that email or username already exists.', 'danger')
            return render_template('auth.html', form=form, title='Register')

        user = User(username=form.username.data, email=form.email.data, role='teacher')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('auth.html', form=form, title='Login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    papers = QuestionPaper.query.filter_by(user_id=current_user.id)\
        .order_by(QuestionPaper.date_created.desc()).all()
    return render_template('dashboard.html', papers=papers)


@app.route('/create_paper', methods=['GET', 'POST'])
@login_required
def create_paper():
    import json
    form = GeneratePaperForm()

    # Build the full topics map (default + any user-added custom topics)
    custom_key = f'custom_topics_{current_user.id}'
    custom_topics = session.get(custom_key, {})
    all_topics = {
        subj: list(topics) + custom_topics.get(subj, [])
        for subj, topics in SUBJECT_TOPICS.items()
    }

    if form.validate_on_submit():
        try:
            # Validate at least one question type is requested
            total = (form.num_mcq.data + form.num_fill.data + form.num_match.data
                     + form.num_short.data + form.num_long.data)
            if total == 0:
                flash('Please include at least one question type.', 'warning')
                return render_template('create_paper.html', form=form,
                                       topics_json=json.dumps(all_topics))

            # Prepare subjects string
            subjects_str = ", ".join(form.subject.data) if isinstance(form.subject.data, list) else form.subject.data

            questions = generate_questions(
                subject=subjects_str,
                topic=form.topic.data,
                level=form.difficulty.data,
                num_mcq=form.num_mcq.data,
                num_fill=form.num_fill.data,
                num_match=form.num_match.data,
                num_short=form.num_short.data,
                num_long=form.num_long.data,
            )

            # Store question-type counts in the paper record as meta JSON
            meta = {
                'num_mcq': form.num_mcq.data,
                'num_fill': form.num_fill.data,
                'num_match': form.num_match.data,
                'num_short': form.num_short.data,
                'num_long': form.num_long.data,
            }

            paper = QuestionPaper(
                subject=subjects_str,
                topic=form.topic.data,
                difficulty=form.difficulty.data,
                content=json.dumps(questions),
                meta=json.dumps(meta),
                author=current_user
            )
            db.session.add(paper)
            db.session.commit()
            flash('Question Paper generated and saved successfully!', 'success')
            return redirect(url_for('view_paper', paper_id=paper.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error generating paper: {str(e)}', 'danger')

    return render_template('create_paper.html', form=form,
                           topics_json=json.dumps(all_topics))


@app.route('/api/add_topic', methods=['POST'])
@csrf.exempt
@login_required
def api_add_topic():
    """Persist a user-defined topic for a subject into the session."""
    import json
    data = request.get_json(force=True)
    subject = (data.get('subject') or '').strip()
    topic = (data.get('topic') or '').strip()

    if not subject or not topic:
        return jsonify({'ok': False, 'error': 'Subject and topic are required.'}), 400
    if subject not in SUBJECT_TOPICS:
        return jsonify({'ok': False, 'error': 'Unknown subject.'}), 400
    if len(topic) > 150:
        return jsonify({'ok': False, 'error': 'Topic too long (max 150 chars).'}), 400

    custom_key = f'custom_topics_{current_user.id}'
    custom = session.get(custom_key, {})
    if subject not in custom:
        custom[subject] = []
    # Avoid duplicates (case-insensitive)
    existing = [t.lower() for t in SUBJECT_TOPICS[subject]] + [t.lower() for t in custom[subject]]
    if topic.lower() in existing:
        return jsonify({'ok': False, 'error': 'Topic already exists.'}), 409
    custom[subject].append(topic)
    session[custom_key] = custom
    session.modified = True
    return jsonify({'ok': True, 'topic': topic})


@app.route('/paper/<int:paper_id>')
@login_required
def view_paper(paper_id):
    paper = db.session.get(QuestionPaper, paper_id)
    if paper is None:
        flash('Paper not found.', 'danger')
        return redirect(url_for('dashboard'))

    import json
    try:
        questions = json.loads(paper.content)
    except (json.JSONDecodeError, TypeError):
        questions = {}
        flash('Error loading paper content.', 'warning')

    return render_template('paper.html', paper=paper, questions=questions)


@app.route('/paper/<int:paper_id>/delete', methods=['POST'])
@login_required
def delete_paper(paper_id):
    paper = db.session.get(QuestionPaper, paper_id)
    if paper is None:
        flash('Paper not found.', 'danger')
        return redirect(url_for('dashboard'))
    if paper.user_id != current_user.id:
        flash('You are not allowed to delete this paper.', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(paper)
    db.session.commit()
    flash('Paper deleted successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/download_pdf/<int:paper_id>')
@login_required
def download_pdf(paper_id):
    paper = db.session.get(QuestionPaper, paper_id)
    if paper is None:
        flash('Paper not found.', 'danger')
        return redirect(url_for('dashboard'))

    import json
    try:
        questions = json.loads(paper.content)
    except (json.JSONDecodeError, TypeError):
        flash('Error reading paper content.', 'danger')
        return redirect(url_for('dashboard'))

    html_content = render_template('pdf_template.html', paper=paper, questions=questions)
    pdf = save_as_pdf(html_content)
    if pdf:
        filename = (f"QuestionMaster_{paper.subject}_{paper.topic}.pdf"
                    .replace(' ', '_').replace('/', '-'))
        return send_file(pdf, as_attachment=True, download_name=filename, mimetype='application/pdf')
    else:
        flash('Error generating PDF. Please try again.', 'danger')
        return redirect(url_for('view_paper', paper_id=paper.id))


def _auto_migrate():
    """
    Lightweight migration: adds any columns that exist in the ORM models
    but are missing from the SQLite database. Runs safely every startup.
    """
    from sqlalchemy import inspect, text
    inspector = inspect(db.engine)

    for table_name, model in [('question_paper', QuestionPaper), ('user', User)]:
        try:
            existing_cols = {col['name'] for col in inspector.get_columns(table_name)}
            mapper_cols = {col.name for col in model.__table__.columns}
            missing = mapper_cols - existing_cols
            for col_name in missing:
                col = model.__table__.columns[col_name]
                col_type = col.type.compile(db.engine.dialect)
                nullable = '' if not col.nullable else ' NULL'
                with db.engine.connect() as conn:
                    conn.execute(text(f'ALTER TABLE "{table_name}" ADD COLUMN "{col_name}" {col_type}{nullable}'))
                    conn.commit()
                print(f'[Migration] Added column "{col_name}" to table "{table_name}"')
        except Exception as e:
            print(f'[Migration] Skipped {table_name}: {e}')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        _auto_migrate()
    app.run(debug=True)

