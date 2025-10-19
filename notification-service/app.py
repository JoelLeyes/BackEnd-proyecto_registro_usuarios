from flask import Flask, request, jsonify
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.example.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USER = os.environ.get('EMAIL_USER', 'notificaciones@practico.com')
EMAIL_PASS = os.environ.get('EMAIL_PASS', '')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')


@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    email = data.get('email')
    usuario_id = data.get('id')

    subject = f"[Notificación] Nuevo usuario creado: {nombre}"
    body = f"Se ha creado un nuevo usuario:\n\nID: {usuario_id}\nNombre: {nombre}\nEmail: {email}\n"

    # Enviar correo
    try:
        msg = EmailMessage()
        msg['From'] = EMAIL_USER
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = subject
        msg.set_content(body)

        if EMAIL_PASS:
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)
        else:
            # Si no hay credenciales, simulamos envío (console)
            print('[Notification-Service] Simulated send:\n', body)

        return jsonify({'status': 'sent'}), 200
    except Exception as e:
        print('[Notification-Service] Error sending email:', e)
        return jsonify({'status': 'error', 'detail': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
