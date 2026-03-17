from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                     SelectField, SelectMultipleField, IntegerField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

# ── B.Tech CSE Syllabus ────────────────────────────────────────────────────────
# Organized by semester → subject
CSE_SYLLABUS = {
    # Semester 1
    "Mathematics I (Calculus & Linear Algebra)": "Sem 1",
    "Physics": "Sem 1",
    "Programming in C": "Sem 1",
    "Engineering Graphics": "Sem 1",

    # Semester 2
    "Mathematics II (Differential Equations)": "Sem 2",
    "Chemistry": "Sem 2",
    "Data Structures": "Sem 2",
    "Digital Electronics": "Sem 2",

    # Semester 3
    "Discrete Mathematics": "Sem 3",
    "Object Oriented Programming (Java)": "Sem 3",
    "Computer Organization & Architecture": "Sem 3",
    "Probability & Statistics": "Sem 3",

    # Semester 4
    "Design & Analysis of Algorithms": "Sem 4",
    "Operating Systems": "Sem 4",
    "Database Management Systems": "Sem 4",
    "Theory of Computation": "Sem 4",

    # Semester 5
    "Computer Networks": "Sem 5",
    "Software Engineering": "Sem 5",
    "Compiler Design": "Sem 5",
    "Microprocessors & Embedded Systems": "Sem 5",

    # Semester 6
    "Artificial Intelligence": "Sem 6",
    "Machine Learning": "Sem 6",
    "Web Technologies": "Sem 6",
    "Information Security": "Sem 6",

    # Semester 7
    "Cloud Computing": "Sem 7",
    "Big Data Analytics": "Sem 7",
    "Internet of Things (IoT)": "Sem 7",
    "Mobile Application Development": "Sem 7",

    # Semester 8
    "Deep Learning": "Sem 8",
    "Natural Language Processing": "Sem 8",
    "Distributed Systems": "Sem 8",
    "Project & Seminar": "Sem 8",
}

SUBJECT_CHOICES = [
    (subject, subject)
    for subject, sem in CSE_SYLLABUS.items()
]

# ── Default topics per subject ─────────────────────────────────────────────────
SUBJECT_TOPICS = {
    "Mathematics I (Calculus & Linear Algebra)": [
        "Limits & Continuity", "Differentiation", "Integration Techniques",
        "Partial Derivatives", "Multiple Integrals", "Vector Calculus",
        "Matrices & Determinants", "Eigenvalues & Eigenvectors",
        "Linear Transformations", "Taylor & Maclaurin Series",
    ],
    "Physics": [
        "Mechanics & Newton's Laws", "Work, Energy & Power",
        "Oscillations & Waves", "Thermodynamics", "Electrostatics",
        "Current Electricity", "Magnetic Fields", "Optics",
        "Modern Physics", "Quantum Mechanics Basics",
    ],
    "Programming in C": [
        "Data Types & Variables", "Control Structures", "Functions & Recursion",
        "Arrays & Strings", "Pointers & Memory Management",
        "Structures & Unions", "File Handling", "Dynamic Memory Allocation",
        "Preprocessor Directives", "Bitwise Operations",
    ],
    "Engineering Graphics": [
        "Orthographic Projections", "Isometric Views",
        "Sectional Views", "Development of Surfaces",
        "Intersection of Solids", "Computer Aided Drafting (CAD)",
    ],
    "Mathematics II (Differential Equations)": [
        "First Order ODEs", "Second Order ODEs", "Laplace Transforms",
        "Fourier Series", "Partial Differential Equations",
        "Numerical Methods for ODEs", "Power Series Solutions",
        "Boundary Value Problems",
    ],
    "Chemistry": [
        "Atomic Structure", "Chemical Bonding", "Thermodynamics",
        "Chemical Kinetics", "Electrochemistry", "Polymers",
        "Corrosion & Prevention", "Water Treatment",
        "Spectroscopic Methods", "Nanomaterials",
    ],
    "Data Structures": [
        "Arrays & Linked Lists", "Stacks & Queues", "Trees & Binary Trees",
        "Binary Search Trees", "AVL Trees", "Heaps & Priority Queues",
        "Hashing & Hash Tables", "Graphs & Graph Traversals",
        "Sorting Algorithms", "Searching Algorithms",
    ],
    "Digital Electronics": [
        "Number Systems & Codes", "Boolean Algebra & Logic Gates",
        "Combinational Circuits", "Multiplexers & Demultiplexers",
        "Flip-Flops & Latches", "Sequential Circuits",
        "Counters & Registers", "Memory Devices",
        "Programmable Logic Devices", "A/D and D/A Conversion",
    ],
    "Discrete Mathematics": [
        "Sets, Relations & Functions", "Propositional Logic",
        "Predicate Logic", "Proof Techniques",
        "Graph Theory Basics", "Trees & Spanning Trees",
        "Counting & Combinatorics", "Recurrence Relations",
        "Algebraic Structures", "Lattices & Boolean Algebra",
    ],
    "Object Oriented Programming (Java)": [
        "Classes & Objects", "Inheritance & Polymorphism",
        "Abstraction & Encapsulation", "Interfaces & Abstract Classes",
        "Exception Handling", "Collections Framework",
        "Generics", "Multithreading",
        "File I/O & Streams", "Java 8 Features (Lambdas, Streams)",
    ],
    "Computer Organization & Architecture": [
        "Data Representation & Number Systems", "ALU Design",
        "Instruction Set Architecture", "CPU Design & Pipelining",
        "Memory Hierarchy & Cache", "Virtual Memory",
        "I/O Organization", "Interrupts & DMA",
        "RISC vs CISC", "Parallel Processing",
    ],
    "Probability & Statistics": [
        "Probability Theory & Axioms", "Random Variables",
        "Probability Distributions", "Binomial & Poisson Distribution",
        "Normal Distribution", "Sampling Distributions",
        "Estimation & Confidence Intervals", "Hypothesis Testing",
        "Regression Analysis", "Correlation",
    ],
    "Design & Analysis of Algorithms": [
        "Asymptotic Notations", "Divide & Conquer",
        "Greedy Algorithms", "Dynamic Programming",
        "Graph Algorithms (BFS, DFS)", "Shortest Path Algorithms",
        "Minimum Spanning Trees", "NP-Completeness",
        "Backtracking", "Branch & Bound",
    ],
    "Operating Systems": [
        "Process Management", "CPU Scheduling Algorithms",
        "Process Synchronization", "Deadlocks",
        "Memory Management", "Paging & Segmentation",
        "Virtual Memory & Thrashing", "File Systems",
        "I/O Management", "Security & Protection",
    ],
    "Database Management Systems": [
        "ER Model & Schema Design", "Relational Model",
        "SQL Queries & Joins", "Normalization (1NF–BCNF)",
        "Transaction Management", "ACID Properties",
        "Concurrency Control", "Indexing & Hashing",
        "Query Optimization", "NoSQL Databases",
    ],
    "Theory of Computation": [
        "Finite Automata (DFA & NFA)", "Regular Expressions",
        "Context-Free Grammars", "Pushdown Automata",
        "Turing Machines", "Decidability",
        "Undecidability & Halting Problem", "Complexity Classes (P, NP)",
        "NP-Completeness & Reductions", "Chomsky Hierarchy",
    ],
    "Computer Networks": [
        "OSI Model & TCP/IP Stack", "Physical Layer",
        "Data Link Layer & MAC", "Network Layer & IP Addressing",
        "Routing Algorithms", "Transport Layer (TCP & UDP)",
        "Application Layer Protocols", "DNS & DHCP",
        "Network Security Basics", "Wireless & Mobile Networks",
    ],
    "Software Engineering": [
        "SDLC Models", "Requirements Engineering",
        "Software Design Principles", "UML Diagrams",
        "Software Testing Techniques", "Agile & Scrum",
        "Software Project Management", "Software Metrics",
        "Software Maintenance", "DevOps Basics",
    ],
    "Compiler Design": [
        "Lexical Analysis & Tokenization", "Regular Grammars & DFA",
        "Syntax Analysis (Parsing)", "LL & LR Parsers",
        "Semantic Analysis", "Intermediate Code Generation",
        "Code Optimization", "Code Generation",
        "Symbol Tables", "Error Handling & Recovery",
    ],
    "Microprocessors & Embedded Systems": [
        "8085 Architecture", "8086 Architecture & Addressing Modes",
        "Assembly Language Programming", "Interrupts & Interrupt Service Routines",
        "Memory Interfacing", "I/O Interfacing",
        "Embedded C Programming", "RTOS Basics",
        "ARM Architecture", "Peripheral Devices & Sensors",
    ],
    "Artificial Intelligence": [
        "Problem Solving & Search Strategies", "BFS & DFS",
        "A* Search Algorithm", "Heuristic Search",
        "Game Playing & Minimax", "Knowledge Representation",
        "Propositional & Predicate Logic", "Bayesian Networks",
        "Expert Systems", "Planning & Scheduling",
    ],
    "Machine Learning": [
        "Supervised Learning", "Linear Regression",
        "Logistic Regression", "Decision Trees & Random Forests",
        "Support Vector Machines", "Unsupervised Learning & Clustering",
        "K-Means & DBSCAN", "Dimensionality Reduction (PCA)",
        "Model Evaluation & Cross-Validation", "Ensemble Methods",
    ],
    "Web Technologies": [
        "HTML5 & CSS3", "JavaScript & DOM Manipulation",
        "Responsive Design & Bootstrap", "PHP & Server-Side Scripting",
        "AJAX & RESTful APIs", "React.js Basics",
        "Node.js & Express", "Databases with Web (MySQL, MongoDB)",
        "Web Security (XSS, CSRF, SQL Injection)", "Deployment & Hosting",
    ],
    "Information Security": [
        "Cryptography Basics", "Symmetric Encryption (AES, DES)",
        "Asymmetric Encryption (RSA, ECC)", "Hash Functions & Digital Signatures",
        "Public Key Infrastructure (PKI)", "Network Security Protocols",
        "Firewalls & IDS/IPS", "Malware & Attacks",
        "Ethical Hacking Concepts", "Security Standards & Compliance",
    ],
    "Cloud Computing": [
        "Cloud Service Models (IaaS, PaaS, SaaS)", "Cloud Deployment Models",
        "Virtualization Techniques", "AWS, Azure & GCP Basics",
        "Containerization & Docker", "Kubernetes Orchestration",
        "Cloud Storage & Databases", "Serverless Computing",
        "CloudSecurity & Compliance", "SLAs & Cloud Economics",
    ],
    "Big Data Analytics": [
        "Big Data Characteristics (5 Vs)", "Hadoop Ecosystem",
        "MapReduce Programming", "HDFS Architecture",
        "Apache Spark", "Hive & HBase",
        "Data Ingestion with Kafka & Flume", "Data Visualization",
        "Machine Learning on Big Data", "Real-Time Analytics",
    ],
    "Internet of Things (IoT)": [
        "IoT Architecture & Layers", "Sensors & Actuators",
        "Communication Protocols (MQTT, CoAP)", "Raspberry Pi & Arduino",
        "IoT Security Challenges", "Edge & Fog Computing",
        "Smart Home & Smart City Applications", "Industrial IoT",
        "Cloud Integration for IoT", "IoT Data Analytics",
    ],
    "Mobile Application Development": [
        "Android Architecture", "Activities & Fragments",
        "Layouts & UI Design", "Intents & Navigation",
        "Data Storage (SQLite, SharedPreferences)", "Networking & APIs",
        "Push Notifications & Firebase", "React Native Basics",
        "Flutter Basics", "App Deployment & Play Store",
    ],
    "Deep Learning": [
        "Artificial Neural Networks", "Backpropagation",
        "Convolutional Neural Networks (CNN)", "Recurrent Neural Networks (RNN)",
        "LSTM & GRU", "Generative Adversarial Networks (GAN)",
        "Transfer Learning", "Autoencoders",
        "Attention Mechanisms & Transformers", "Reinforcement Learning Basics",
    ],
    "Natural Language Processing": [
        "Text Preprocessing & Tokenization", "Bag of Words & TF-IDF",
        "Word Embeddings (Word2Vec, GloVe)", "Language Models",
        "Named Entity Recognition (NER)", "Sentiment Analysis",
        "Machine Translation", "Text Summarization",
        "Question Answering Systems", "BERT & GPT Architectures",
    ],
    "Distributed Systems": [
        "Distributed System Characteristics", "Communication Models",
        "Clock Synchronization", "Mutual Exclusion",
        "Consensus Algorithms (Raft, Paxos)", "Replication Strategies",
        "Fault Tolerance & Recovery", "CAP Theorem",
        "MapReduce & Distributed Computing", "Microservices Architecture",
    ],
    "Project & Seminar": [
        "Project Planning & Management", "Literature Survey",
        "System Design & Architecture", "Implementation & Coding",
        "Testing & Validation", "Documentation & Report Writing",
        "Seminar Presentation Skills", "Research Methodology",
    ],
}


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class GeneratePaperForm(FlaskForm):
    subject = SelectMultipleField('Subjects', choices=SUBJECT_CHOICES, validators=[DataRequired()])
    topic = StringField('Specific Topics / Units',
                        validators=[DataRequired(), Length(min=2, max=500)],
                        description='e.g. Binary Trees, TCP/IP Model, Normalization')
    difficulty = SelectField('Difficulty Level', choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], validators=[DataRequired()])

    # ── Question-Type Counts ──────────────────────────────────────────────────
    num_mcq = IntegerField('MCQs', default=5,
                           validators=[NumberRange(min=0, max=20)])
    num_fill = IntegerField('Fill in the Blanks', default=4,
                            validators=[NumberRange(min=0, max=20)])
    num_match = IntegerField('Match the Following (pairs)', default=3,
                             validators=[NumberRange(min=0, max=10)])
    num_short = IntegerField('Short Answer Questions', default=4,
                             validators=[NumberRange(min=0, max=20)])
    num_long = IntegerField('Long Answer Questions', default=2,
                            validators=[NumberRange(min=0, max=10)])

    submit = SubmitField('Generate Question Paper')
