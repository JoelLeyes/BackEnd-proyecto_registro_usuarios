# Backend – Users API (Django)

Aplicación backend del proyecto “Registro de Usuarios”. Expone una API REST para crear y listar usuarios y emite una notificación al servicio de notificaciones cuando se crea un usuario.

- Lenguaje/Framework: Python + Django (5.2.8)
- Base de datos: PostgreSQL (en producción: AWS RDS)
- Contenedor: Docker; imágenes en Amazon ECR
- Orquestación: Kubernetes (Amazon EKS)

## Arquitectura breve
- Endpoint público final: `https://api.<tu-dominio>/api/usuarios/` (ej.: `https://api.labinfra2025.cloud-ip.cc/api/usuarios/`)
- En EKS el Service del backend es `LoadBalancer` (NLB). API Gateway HTTP API apunta al NLB.
- Frontend consume esta API vía `/api/usuarios/`.

## Endpoints principales
- `GET /api/usuarios/` – Lista usuarios
- `POST /api/usuarios/` – Crea usuario; body JSON: `{ "nombre": "...", "email": "...", "telefono": "..." }`

## Requisitos locales
- Python 3.11+ recomendado
- pip ≥ 25

## Ejecución local (desarrollo)
```powershell
# 1) Crear y activar venv (opcional pero recomendado)
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Variables de entorno (credenciales simuladas)
$env:DB_ENGINE = "django.db.backends.sqlite3"      # Para local simple
$env:DB_NAME   = "db.sqlite3"                     # Usar SQLite local por defecto
$env:DB_HOST   = ""                               # Vacío para SQLite
$env:DB_PORT   = ""                               # Vacío para SQLite
$env:SMTP_HOST = "smtp.example.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "notifier@example.com"
$env:SMTP_PASS = "simulated-strong-pass"
$env:NOTIFY_URL = "http://localhost:5001/notify"  # Servicio de notificaciones local

# 4) Migraciones y runserver
cd .\BackEnd
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Pruebas rápidas (local)
```powershell
# Listar usuarios
curl http://127.0.0.1:8000/api/usuarios/

# Crear usuario
curl -X POST http://127.0.0.1:8000/api/usuarios/ `
	-H "Content-Type: application/json" `
	-d '{"nombre":"Juan","email":"juan@example.com","telefono":"099123456"}'
```

## Contenedor Docker
```powershell
# Desde BackEnd-proyecto_registro_usuarios
docker build -t users-api:local .

# Ejecutar (SQLite local)
docker run --rm -p 8000:8000 `
	-e DB_ENGINE=django.db.backends.sqlite3 `
	-e DB_NAME=db.sqlite3 `
	-e SMTP_HOST=smtp.example.com -e SMTP_PORT=587 `
	-e SMTP_USER=notifier@example.com -e SMTP_PASS=simulated-strong-pass `
	-e NOTIFY_URL=http://host.docker.internal:5001/notify `
	users-api:local
```

## Publicación en ECR (placeholders)
```powershell
$AWS_ACCOUNT_ID = "111122223333"
$AWS_REGION     = "us-east-1"
$REPO           = "proyecto/backend"
$IMAGE          = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO:latest"

aws ecr get-login-password --region $AWS_REGION | docker login `
	--username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

docker build -t $IMAGE .
docker push $IMAGE
```

## Despliegue en Kubernetes (EKS)
Manifiestos relevantes en `k8s/` (en el repo raíz del proyecto):
- `k8s/db-secret.yml` (credenciales DB)
- `k8s/db-configmap.yml` (host/puerto DB)
- `k8s/backend-deployment.yml` (Deployment + Service LoadBalancer)

Aplicación:
```powershell
kubectl apply -f k8s/db-secret.yml
kubectl apply -f k8s/db-configmap.yml
kubectl apply -f k8s/backend-deployment.yml
kubectl get svc,pods -o wide
```
En este proyecto, el Service del backend es `LoadBalancer` (NLB). Luego se integra con API Gateway HTTP API y un dominio personalizado.

## Variables de entorno (producción – ejemplo)
Credenciales simuladas; no usar en producción.

- Base de datos (RDS PostgreSQL)
	- `DB_ENGINE=django.db.backends.postgresql`
	- `DB_HOST=db-proyecto.abcxyz.us-east-1.rds.amazonaws.com`
	- `DB_PORT=5432`
	- `DB_NAME=users`
	- `DB_USER=users_app`
	- `DB_PASSWORD=simulated-strong-pass`

- Notificaciones / SMTP
	- `SMTP_HOST=smtp.example.com`
	- `SMTP_PORT=587`
	- `SMTP_USER=notifier@example.com`
	- `SMTP_PASS=simulated-strong-pass`
	- `NOTIFY_URL=http://notificaciones.default.svc.cluster.local:5001/notify`

Estas variables se cargan en Kubernetes desde `Secrets` y `ConfigMaps`.

## Seguridad (SSDLC) – evidencias
- SAST (Bandit) y SCA (pip-audit) sobre el código y dependencias.
- SCA de imagen (Grype) en ECR.
- DAST (OWASP ZAP) sobre endpoints públicos.
Evidencias en `evidencias/security/` del repo raíz (archivos `.txt`, `.json`, `.html`).

## Diagrama y DNS/TLS
- Frontend accesible por ALB (HTTPS) con ACM; redirect HTTP→HTTPS.
- API publicada por API Gateway con dominio `api.<tu-dominio>`.
- RDS privado en la VPC.

## Troubleshooting rápido
- 503 en frontend: verificar Target Group del ALB con targets (instancias EKS + NodePort del frontend).
- `ExpiredToken` en AWS CLI: renovar credenciales del lab y `w32tm /resync`.
- DB conexión: probar desde Pod del backend con `psql` e inspeccionar `DB_*` vía `kubectl describe` en Secret/ConfigMap`.

---
Este README incluye credenciales simuladas a modo de ejemplo. No subir secretos reales.
