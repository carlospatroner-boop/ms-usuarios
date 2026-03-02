from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

# URL interna de Kubernetes (DNS del Cluster)
# Así es como un microservicio encuentra al otro sin salir a internet
API_URL = "http://ms-usuarios-service:80/api/usuarios"

@app.route('/')
def index():
    try:
        # Consumimos el microservicio de Java
        response = requests.get(API_URL, timeout=5)
        users = response.json()
        status = "Conectado ✅"
    except Exception as e:
        users = []
        status = f"Error de conexión ❌: {str(e)}"

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard DevOps</title>
        <style>
            body { font-family: sans-serif; background: #1e1e2e; color: white; padding: 50px; }
            h1 { color: #a6e3a1; }
            .card { background: #313244; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #45475a; }
            th { color: #89b4fa; }
            .status { font-weight: bold; color: #f9e2af; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Dashboard de Microservicios</h1>
            <p>Este servicio (Python) está consumiendo datos del servicio Core (Java).</p>
            <p class="status">Estado del Backend Java: {{ status }}</p>

            <h2>Usuarios Registrados: {{ users|length }}</h2>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Email</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.nombre }}</td>
                        <td>{{ user.email }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, users=users, status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)