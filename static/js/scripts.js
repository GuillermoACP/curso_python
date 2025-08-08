// Función para ejecutar el codigo con Skulpt
function runCode() {
    const code = document.getElementById('code-display').value; // <-- .value para textarea
    const output = document.getElementById('output');
    output.innerHTML = '';

    function outf(text) {
        output.innerHTML += text;
    }

    Sk.configure({
        output: outf,
        read: function(x) {
            if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined) {
                throw "File not found: '" + x + "'";
            }
            return Sk.builtinFiles["files"][x];
        }
    });

    Sk.misceval.asyncToPromise(function() {
        return Sk.importMainWithBody("<stdin>", false, code, true);
    }).then(function(mod) {
        console.log("Código ejecutado correctamente");
    }, function(err) {
        console.error("Error al ejecutar el código:", err);
        output.innerHTML += "<span style='color: red;'>Error: " + err.toString() + "</span>";
    });
}

// Función para mostrar/ocultar el bloque de solución
function showSolution() {
    const solutionContainer = document.getElementById('solution-container');
    if (solutionContainer.style.display === 'none' || solutionContainer.style.display === '') {
        solutionContainer.style.display = 'block'; // Mostrar el bloque de código
    } else {
        solutionContainer.style.display = 'none'; // Ocultar el bloque de código
    }
}