from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

# URL interna de Kubernetes (DNS del Cluster)
# Apuntamos al endpoint correcto
API_URL = "http://ms-usuarios-service:80/api/entregas"

@app.route('/')
def index():
    try:
        # Consumimos el microservicio de Java
        response = requests.get(API_URL, timeout=5)
        entregas = response.json()
        status = "Conectado ✅"
    except Exception as e:
        entregas = []
        status = f"Error de conexión ❌: {str(e)}"

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard de Envíos</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f6; color: #333; padding: 40px; }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 10px; }
            .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            .status { text-align: center; margin-bottom: 30px; font-weight: bold; color: #27ae60; background: #e8f8f5; padding: 10px; border-radius: 5px; display: inline-block; }

            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #3498db; color: white; }
            tr:hover { background-color: #f1f1f1; }

            .badge { padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; color: white; }
            .PENDIENTE { background-color: #f39c12; }
            .ENVIADO { background-color: #3498db; }
            .ENTREGADO { background-color: #27ae60; }
            .CANCELADO { background-color: #c0392b; }

            .empty { text-align: center; color: #888; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div style="text-align: center;">
            <div class="container">
                <h1>📦 Monitor de Entregas</h1>
                <p class="status">Estado del Backend Java: {{ status }}</p>

                {% if entregas %}
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Dirección de Entrega</th>
                                <th>Estado</th>
                                <th>Tracking #</th>
                                <th>Email Cliente</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for entrega in entregas %}
                            <tr>
                                <td>#{{ entrega.id }}</td>
                                <td>{{ entrega.address }}</td>
                                <td><span class="badge {{ entrega.status }}">{{ entrega.status }}</span></td>
                                <td>{{ entrega.trackingNumber or '---' }}</td>
                                <td>{{ entrega.email or '---' }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <p class="empty">No hay entregas registradas en el sistema.</p>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, entregas=entregas, status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)