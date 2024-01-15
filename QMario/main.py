from flask import Flask, request, jsonify
from flask_cors import CORS
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute

app = Flask(__name__)
CORS(app)


def set_character_superposition():
    qr = QuantumRegister(1)
    cr = ClassicalRegister(1)
    qc = QuantumCircuit(qr, cr, name="qc1")
    qc.h(0)
    qc.measure(0, 0)

    return qc, "1"


# Extra Feature. Not fully implemented
def activate_quantum_tunnel():
    qr = QuantumRegister(1)
    cr = ClassicalRegister(1)
    qc = QuantumCircuit(qr, cr, name="qc2")
    qc.h(0)
    qc.ry(0.1, 0)
    qc.measure(0, 0)

    return qc


from random import randrange
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, Aer


def obstacle_assignment():
    q = QuantumRegister(2, "q")  # quantum register with 2 qubits
    c = ClassicalRegister(2)  # classical register with 2 bits

    qc = QuantumCircuit(q, c)  # quantum circuit with quantum and classical registers
    qc.h(q[0])
    qc.h(q[1])

    qc.measure_all()
    # display(qc.draw(output='mpl',reverse_bits=True))

    # execute the circuit 100 times in the local simulator
    job = execute(qc, Aer.get_backend('qasm_simulator'), shots=100)
    counts = job.result().get_counts(qc)

    res = 0
    if max(counts['10 00'], counts['01 00'], counts['00 00'], counts['11 00']) == counts['00 00']:
        res = 1  # Small
    elif max(counts['10 00'], counts['01 00'], counts['00 00'], counts['11 00']) == counts['01 00']:
        res = 2  # Medium
    elif max(counts['10 00'], counts['01 00'], counts['00 00'], counts['11 00']) == counts['10 00']:
        res = 3  # Big
    else:
        res = 4  # Too Big

    return res


@app.route("/set_superposition")
def set_superposition():
    qc, is_superposition = set_character_superposition()
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, simulator, shots=1024).result()
    counts = result.get_counts(qc)

    return counts


@app.route("/place_obstacle")
def place_obstacle():
    obstacle = obstacle_assignment()
    print(str(obstacle))
    return str(obstacle)


# Extra Feature. Not fully implemented
@app.route("/quantum_tunnel")
def quantum_tunnel():
    qc = activate_quantum_tunnel()
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, simulator, shots=1024).result()
    counts = result.get_counts(qc)

    return counts


# If the character in the game hits an obstacle, a "True" value is sent
# to the server and is printed to the console ("print(value)")
# This can eventually be further used to apply a measurement in a circuit
@app.route("/hit_obstacle", methods=["POST"])
def hit_obstacle():
    data = request.form or request.json
    value = data['hit_obstacle']
    print(value)


if __name__ == '__main__':
    app.run()
