<div align="center">
  <h1>🛡️ Error Explainer</h1>
  <p><i>The "Friendly Compiler" that makes programming errors understandable for beginners.</i></p>

  <p>
    <a href="https://github.com/rahul2112-code/Error-Explainer/commits/main">
      <img src="https://img.shields.io/github/last-commit/rahul2112-code/Error-Explainer" alt="Last Commit">
    </a>
    <a href="https://github.com/rahul2112-code/Error-Explainer/stargazers">
      <img src="https://img.shields.io/github/stars/rahul2112-code/Error-Explainer?style=social" alt="Stars">
    </a>
  </p>
</div>

<hr />

## 📖 Overview

Learning to program is hard enough without having to decipher cryptic compiler errors. **Error Explainer** acts as a middleman between you and the standard compilers (like `gcc` and `javac`). 

Whenever your code fails to compile, this application catches the raw output, parses it using advanced pattern matching, and translates it into **plain, actionable English**.

### ✨ Key Features

- **🧠 Multi-Language Support:** Beautifully translates both C and Java compiler errors.
- **🎯 Friendly Translations:** Replaces confusing jargon like `expected ';' before 'return'` with simple instructions like `You forgot a semicolon (;) on the previous line`.
- **📈 Confidence Tracking System:** Learns from user feedback! If an explanation is rated highly, the system boosts its confidence score for future translations.
- **🖥️ Interactive Web UI:** Write, compile, and debug your code seamlessly in a clean browser interface.

---

## 🛠️ Technology Stack

- **Backend:** Python 3, Flask framework
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Compilers Integrated:** `gcc` (for C), `javac` (for Java)
- **Data Storage:** JSON (for pattern mapping and statistics)

---

## 🚀 Setup & Installation

Follow these steps to run the Error Explainer locally on your machine.

### Prerequisites
Make sure you have the following installed on your system:
- [Python 3.x](https://www.python.org/downloads/)
- **GCC** (usually pre-installed on Linux/Mac. For Windows, install MinGW).
- **Java Development Kit (JDK)**.

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rahul2112-code/Error-Explainer.git
   cd Error-Explainer
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the environment:**
   - On **macOS/Linux**: `source venv/bin/activate`
   - On **Windows**: `venv\Scripts\activate`

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the server:**
   ```bash
   python app.py
   ```
   Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🏗️ Project Architecture

```text
Error-Explainer/
├── app.py                      # Main Flask application and API routing
├── friendlyCompiler.py         # Core C error parsing and translation logic
├── error_patterns.json         # Database of regex patterns for C errors
├── confidence_stats.json       # Usage statistics and feedback tracking
├── java_compiler/              # Module for handling Java specifically
│   ├── friendlyJavaCompiler.py # Core Java parsing logic
│   └── java_error_patterns.json# Database of Java patterns
├── static/                     # CSS stylesheets and client-side JavaScript
└── templates/                  # HTML templates for the web interface
```

### How the Translation Works
1. Code is received via the web interface and written to a temporary file.
2. A subprocess triggers the respective compiler (`gcc` or `javac`).
3. If an error occurs, the raw standard error output (`stderr`) is intercepted.
4. The output is run through hundreds of Regex patterns stored in our `*_error_patterns.json` files.
5. Once a match is found, the system formats a dynamic, beginner-friendly string and returns it to the UI!

---

## 🔮 Future Enhancements
- [ ] Add support for Python Tracebacks and C++ errors.
- [ ] Implement AI-driven error explanation as a fallback for unknown patterns.
- [ ] Add a dark mode toggle to the user interface.
- [ ] Support multiple files and project structures inside the web editor.

---

## 🤝 Contributing

Contributions are always welcome! If you've found a compiler error that Error Explainer doesn't recognize yet, please consider adding a pattern for it.

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/NewPattern`).
3. Commit your Changes (`git commit -m 'Add some NewPattern'`).
4. Push to the Branch (`git push origin feature/NewPattern`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. Feel free to use, modify, and distribute this project as you see fit.
