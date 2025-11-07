# KC Liberando Productos - Práctica Final
## Simple Server - Aplicación FastAPI con CI/CD y Monitorización

[![Test](https://github.com/jpalenz77/KC-liberando-productos-practica-final/actions/workflows/test.yml/badge.svg)](https://github.com/jpalenz77/KC-liberando-productos-practica-final/actions/workflows/test.yml)
[![Release](https://github.com/jpalenz77/KC-liberando-productos-practica-final/actions/workflows/release.yml/badge.svg)](https://github.com/jpalenz77/KC-liberando-productos-practica-final/actions/workflows/release.yml)

---

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Endpoints Implementados](#-endpoints-implementados)
3. [Tests Unitarios](#-tests-unitarios)
4. [CI/CD Pipeline](#-cicd-pipeline)
5. [Helm Chart](#-helm-chart)
6. [Monitorización con Prometheus](#-monitorización-con-prometheus)
7. [Alertas con Alertmanager](#-alertas-con-alertmanager)
8. [Dashboard de Grafana](#-dashboard-de-grafana)
9. [Guía de Despliegue](#-guía-de-despliegue)
10. [Troubleshooting](#-troubleshooting)

---

## 📖 Descripción del Proyecto

Este proyecto implementa una aplicación web simple usando **FastAPI** con los siguientes componentes:

- **Aplicación**: Servidor web con múltiples endpoints
- **Tests**: Cobertura del 89% con pytest
- **CI/CD**: GitHub Actions para testing y release
- **Containerización**: Docker image publicada en GHCR
- **Orquestación**: Helm chart para Kubernetes
- **Monitorización**: Prometheus + Grafana + Alertmanager

---

## 🚀 Endpoints Implementados

La aplicación expone los siguientes endpoints:

### 1. **GET /** - Main Endpoint
```bash
curl http://localhost:8081/
# Response: {"msg": "Hello World"}
```

### 2. **GET /bye** - Nuevo Endpoint (Práctica Final)
```bash
curl http://localhost:8081/bye
# Response: {"msg": "Bye Bye"}
```

### 3. **GET /health** - Health Check
```bash
curl http://localhost:8081/health
# Response: {"health": "ok"}
```

### 4. **GET /metrics** - Métricas de Prometheus
```bash
curl http://localhost:8081/metrics
# Response: métricas en formato Prometheus
```

**Métricas expuestas:**
- `server_requests_total` - Total de peticiones al servidor
- `main_requests_total` - Peticiones al endpoint `/`
- `bye_requests_total` - Peticiones al endpoint `/bye` ⭐ NUEVO
- `healthcheck_requests_total` - Peticiones al endpoint `/health`

---

## 🧪 Tests Unitarios

### Estructura de Tests
```
tests/
├── __init__.py
├── conftest.py          # Configuración de pytest
└── app_test.py          # Tests de los endpoints
```

### Tests Implementados

Los tests cubren todos los endpoints con un **89% de cobertura**:

1. ✅ `test_read_health()` - Verifica endpoint `/health`
2. ✅ `test_read_main()` - Verifica endpoint `/`
3. ✅ `test_read_bye()` - Verifica endpoint `/bye` ⭐ NUEVO
4. ✅ `test_metrics()` - Verifica endpoint `/metrics` y todas las métricas

### Ejecutar Tests Localmente
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests con cobertura
pytest --cov --cov-report=term -v

# Ver reporte HTML
pytest --cov --cov-report=html
open htmlcov/index.html
```

### Resultado Esperado
```
tests/app_test.py::TestSimpleServer::test_read_health PASSED      [ 25%]
tests/app_test.py::TestSimpleServer::test_read_main PASSED        [ 50%]
tests/app_test.py::TestSimpleServer::test_read_bye PASSED         [ 75%]
tests/app_test.py::TestSimpleServer::test_metrics PASSED          [100%]

---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                          Stmts   Miss  Cover
-----------------------------------------------------------
src/__init__.py                   0      0   100%
src/application/__init__.py       0      0   100%
src/application/app.py           36      4    89%
-----------------------------------------------------------
TOTAL                            36      4    89%
```

---

## 🔄 CI/CD Pipeline

El proyecto implementa dos workflows de GitHub Actions:

### 1. Testing Pipeline (`.github/workflows/test.yml`)

**Trigger:** Push o Pull Request a cualquier rama

**Pasos:**
1. Checkout del código
2. Setup de Python 3.11.8
3. Instalación de dependencias
4. Ejecución de tests con coverage
5. Generación de reportes de cobertura
6. Comentario automático en PRs con el coverage

**Ejemplo de ejecución:**
```bash
# Ver en GitHub Actions
https://github.com/jpalenz77/KC-liberando-productos-practica-final/actions
```

**Resultado esperado:**
- ✅ Tests passing
- ✅ Coverage > 70%
- ✅ Comentario automático en PR con cobertura

### 2. Build & Push Pipeline (`.github/workflows/release.yml`)

**Trigger:** Push de tags con formato `v*` (ejemplo: `v1.0.0`)

**Pasos:**
1. Checkout del código
2. Setup de Docker Buildx
3. Login en GitHub Container Registry (GHCR)
4. Extracción de metadata (tags)
5. Build y push de la imagen Docker

**Estrategia de tags:**

Para un tag `v1.2.3`, se generan automáticamente:
- `ghcr.io/jpalenz77/kc-liberando-productos-practica-final:1.2.3`
- `ghcr.io/jpalenz77/kc-liberando-productos-practica-final:1.2`
- `ghcr.io/jpalenz77/kc-liberando-productos-practica-final:1`
- `ghcr.io/jpalenz77/kc-liberando-productos-practica-final:latest`

**Crear un release:**
```bash
# Crear tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag (dispara el workflow)
git push origin v1.0.0

# Verificar la imagen publicada
docker pull ghcr.io/jpalenz77/kc-liberando-productos-practica-final:latest
```

---

## ⎈ Helm Chart

### Estructura del Chart
```
helm/simple-server/
├── Chart.yaml              # Metadata del chart
├── values.yaml             # Valores configurables
└── templates/
    ├── _helpers.tpl        # Funciones helper
    ├── deployment.yaml     # Deployment con la app
    ├── service.yaml        # Service (ClusterIP)
    ├── serviceaccount.yaml # ServiceAccount
    ├── hpa.yaml           # HorizontalPodAutoscaler
    ├── ingress.yaml       # Ingress (opcional)
    ├── service_monitor.yaml # ServiceMonitor (Prometheus)
    └── dockerhub_access.yaml # Secret para GHCR
```

### Características del Chart

- ✅ **Deployment**: 1-100 réplicas con autoscaling
- ✅ **Service**: Expone puerto 8081 (app) y 8000 (metrics)
- ✅ **HPA**: Autoscaling basado en CPU (70%) y memoria (70%)
- ✅ **ServiceMonitor**: Integración automática con Prometheus
- ✅ **Health Checks**: Liveness y Readiness probes
- ✅ **Resources**: Limits y requests configurados

### Instalación del Chart
```bash
# Añadir repositorio de Helm (si aún no está)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Instalar la aplicación
helm install simple-server ./helm/simple-server \
  --namespace simple-server \
  --create-namespace \
  --set image.repository=ghcr.io/jpalenz77/kc-liberando-productos-practica-final \
  --set image.tag=latest
```

### Verificar el despliegue
```bash
# Ver pods
kubectl get pods -n simple-server

# Ver servicios
kubectl get svc -n simple-server

# Ver HPA
kubectl get hpa -n simple-server

# Ver ServiceMonitor
kubectl get servicemonitor -n simple-server

# Logs de la aplicación
kubectl logs -n simple-server -l app.kubernetes.io/name=simple-server -f
```

### Port-forward para acceder
```bash
# Aplicación
kubectl port-forward -n simple-server svc/simple-server 8081:8081

# Probar endpoints
curl http://localhost:8081/
curl http://localhost:8081/bye
curl http://localhost:8081/health
curl http://localhost:8081/metrics
```

---

## 📊 Monitorización con Prometheus

### Instalación de kube-prometheus-stack
```bash
# Crear namespace
kubectl create namespace monitoring

# Instalar Prometheus Operator + Grafana + Alertmanager
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values monitoring/kube-prometheus-stack/values.yaml
```

### Verificar instalación
```bash
# Ver todos los pods de monitoring
kubectl get pods -n monitoring

# Deberías ver:
# - prometheus-operator
# - prometheus-prometheus-kube-prometheus-prometheus-0
# - alertmanager-prometheus-kube-prometheus-alertmanager-0
# - prometheus-grafana-xxx
# - prometheus-kube-state-metrics-xxx
# - prometheus-prometheus-node-exporter-xxx
```

### Acceder a Prometheus
```bash
# Port-forward
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Abrir en navegador
open http://localhost:9090
```

### Verificar que las métricas se están recolectando

1. Ve a **Status → Targets**
2. Busca el job `simple-server`
3. Debería estar en estado **UP**

### Queries útiles en Prometheus
```promql
# Total de requests
server_requests_total

# Rate de requests por segundo
rate(server_requests_total[5m])

# Requests al endpoint /bye
bye_requests_total

# Rate del endpoint /bye
rate(bye_requests_total[5m])

# Comparar todos los endpoints
sum by (endpoint) (rate(server_requests_total[5m]))

# Reinicios de la aplicación
kube_pod_container_status_restarts_total{pod=~".*simple-server.*"}
```

---

## 🚨 Alertas con Alertmanager

### Configuración de Slack

1. **Crear canal en Slack**: `#jpalenz-prometheus-alarms`
2. **Crear Incoming Webhook**:
   - Ve a https://api.slack.com/apps
   - Create New App → From scratch
   - Nombre: "Prometheus Alertmanager"
   - Incoming Webhooks → Activate → Add New Webhook
   - Copia la URL del webhook

3. **Configurar en values.yaml**:
```yaml
   alertmanager:
     config:
       global:
         slack_api_url: 'https://hooks.slack.com/services/TU-WEBHOOK-AQUI'
       receivers:
         - name: 'slack-critical'
           slack_configs:
             - channel: '#jpalenz-prometheus-alarms'
```

### Alertas Configuradas

#### Alertas CRITICAL (🔴):

| Alerta | Condición | Duración |
|--------|-----------|----------|
| `SimpleServerDown` | Pod caído | 1 min |
| `SimpleServerCPUThrottlingHigh` | CPU throttling > 25% | 5 min |
| `SimpleServerConsumingMoreThanRequest` | Memoria > request | 2 min |
| `SimpleServerMemoryLimitReached` | Memoria > 90% del límite | 1 min |

#### Alertas HIGH (🟠):

| Alerta | Condición | Duración |
|--------|-----------|----------|
| `SimpleServerCPUConsumingMoreThanRequest` | CPU > request | 2 min |
| `SimpleServerHighRequestRate` | > 100 req/s | 5 min |
| `SimpleServerNoRequests` | Sin requests | 10 min |
| `SimpleServerPodRestarting` | Pod reiniciando | 5 min |

### Probar las alertas

#### Opción 1: Escalar a 0 (SimpleServerDown)
```bash
# Escalar a 0 réplicas
kubectl scale deployment simple-server -n simple-server --replicas=0

# Esperar ~2 minutos → Recibirás alerta en Slack

# Restaurar
kubectl scale deployment simple-server -n simple-server --replicas=2
```

#### Opción 2: Generar carga CPU
```bash
# Instalar stress
kubectl run stress-test -n simple-server \
  --image=polinux/stress \
  --rm -it --restart=Never \
  -- stress --cpu 2 --timeout 300s
```

### Acceder a Alertmanager
```bash
# Port-forward
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-alertmanager 9093:9093

# Abrir en navegador
open http://localhost:9093
```

---

## 📈 Dashboard de Grafana

### Acceder a Grafana
```bash
# Port-forward
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Abrir en navegador
open http://localhost:3000

# Credenciales:
# User: admin
# Password: prom-operator
```

### Importar Dashboard

**Opción 1: Mediante ConfigMap (Automático)**
```bash
# Aplicar el ConfigMap
kubectl apply -f monitoring/grafana/simple-server-dashboard-configmap.yaml

# El dashboard aparecerá automáticamente en Grafana
```

**Opción 2: Import Manual**

1. En Grafana, click en **+** → **Import**
2. Click en **Upload JSON file**
3. Selecciona `monitoring/grafana/dashboards/simple-server-dashboard.json`
4. Selecciona datasource: **Prometheus**
5. Click **Import**

### Paneles del Dashboard

El dashboard **"Simple Server - Application Metrics"** incluye:

#### Fila 1 - Contadores (Gauges):
1. **Total Requests** - Total de peticiones al servidor
2. **Main Endpoint (/) Calls** - Llamadas a `/`
3. **Bye Endpoint (/bye) Calls** - Llamadas a `/bye` ⭐
4. **Application Restarts** - Número de reinicios ⭐

#### Fila 2 - Gráfico de Rate:
5. **Request Rate by Endpoint** - Peticiones/segundo por endpoint

#### Fila 3 - Gráfico Acumulativo:
6. **Cumulative Requests by Endpoint** - Requests totales acumulados

### Generar Tráfico para Poblar el Dashboard
```bash
# Script para generar tráfico
kubectl port-forward -n simple-server svc/simple-server 8081:8081 &

for i in {1..1000}; do
  curl -s http://localhost:8081/ > /dev/null
  curl -s http://localhost:8081/bye > /dev/null
  curl -s http://localhost:8081/health > /dev/null
  sleep 0.1
done
```

### Exportar Dashboard

Si haces cambios en el dashboard:

1. Click en el icono de configuración (⚙️) → **JSON Model**
2. Copia el JSON
3. Guarda en `monitoring/grafana/dashboards/simple-server-dashboard.json`

---

## 🛠️ Guía de Despliegue

### Requisitos Previos

- Docker
- Kubernetes (Minikube, Kind, K3s, o cluster real)
- kubectl configurado
- Helm 3.x
- Git

### Paso 1: Iniciar Minikube
```bash
# Iniciar con recursos suficientes
minikube start --cpus=4 --memory=8192 --driver=docker

# Habilitar addons
minikube addons enable metrics-server

# Verificar
kubectl get nodes
```

### Paso 2: Instalar Prometheus Stack
```bash
# Añadir repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Crear namespace
kubectl create namespace monitoring

# Instalar (IMPORTANTE: configurar Slack webhook antes)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values monitoring/kube-prometheus-stack/values.yaml

# Esperar a que todos los pods estén ready
kubectl get pods -n monitoring -w
```

### Paso 3: Desplegar Simple Server
```bash
# Crear namespace
kubectl create namespace simple-server

# Instalar con Helm
helm install simple-server ./helm/simple-server \
  --namespace simple-server \
  --set image.repository=ghcr.io/jpalenz77/kc-liberando-productos-practica-final \
  --set image.tag=latest \
  --set metrics.enabled=true

# Verificar
kubectl get pods -n simple-server
kubectl get svc -n simple-server
kubectl get servicemonitor -n simple-server
```

### Paso 4: Aplicar Dashboard de Grafana
```bash
# Aplicar ConfigMap con el dashboard
kubectl apply -f monitoring/grafana/simple-server-dashboard-configmap.yaml

# Verificar
kubectl get configmap -n monitoring simple-server-dashboard
```

### Paso 5: Acceder a las Interfaces
```bash
# Terminal 1: Aplicación
kubectl port-forward -n simple-server svc/simple-server 8081:8081

# Terminal 2: Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Terminal 3: Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Terminal 4: Alertmanager
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-alertmanager 9093:9093
```

**URLs:**
- Aplicación: http://localhost:8081
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin / prom-operator)
- Alertmanager: http://localhost:9093

### Paso 6: Verificar que Todo Funciona
```bash
# 1. Probar endpoints
curl http://localhost:8081/
curl http://localhost:8081/bye
curl http://localhost:8081/health
curl http://localhost:8081/metrics

# 2. Verificar métricas en Prometheus
# Ir a http://localhost:9090 → Graph
# Query: server_requests_total

# 3. Ver dashboard en Grafana
# Ir a http://localhost:3000 → Dashboards → Simple Server - Application Metrics

# 4. Generar una alerta de prueba
kubectl scale deployment simple-server -n simple-server --replicas=0
# Esperar 2 minutos → Deberías recibir alerta en Slack
kubectl scale deployment simple-server -n simple-server --replicas=2
```

---

## 🔍 Troubleshooting

### Problema: Tests fallan localmente
```bash
# Solución: Verificar entorno virtual y dependencias
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest --cov -v
```

### Problema: Docker image no se construye
```bash
# Verificar Dockerfile
docker build -t simple-server:test .

# Ver logs de build
docker build -t simple-server:test . --progress=plain
```

### Problema: Pods no inician en Kubernetes
```bash
# Ver eventos del pod
kubectl describe pod -n simple-server <pod-name>

# Ver logs
kubectl logs -n simple-server <pod-name>

# Ver si hay problemas con la imagen
kubectl get events -n simple-server --sort-by='.lastTimestamp'
```

### Problema: Prometheus no encuentra targets
```bash
# Verificar ServiceMonitor
kubectl get servicemonitor -n simple-server -o yaml

# Verificar que el Service tiene el label correcto
kubectl get svc -n simple-server -o yaml

# Ver logs de Prometheus
kubectl logs -n monitoring prometheus-prometheus-kube-prometheus-prometheus-0
```

### Problema: Dashboard no aparece en Grafana
```bash
# Verificar ConfigMap
kubectl get configmap -n monitoring simple-server-dashboard

# Verificar labels
kubectl get configmap -n monitoring simple-server-dashboard -o yaml | grep labels -A 5

# Reiniciar Grafana
kubectl rollout restart deployment -n monitoring prometheus-grafana
```

### Problema: Alertas no llegan a Slack
```bash
# Verificar configuración de Alertmanager
kubectl get secret -n monitoring alertmanager-prometheus-kube-prometheus-alertmanager -o yaml

# Ver logs de Alertmanager
kubectl logs -n monitoring alertmanager-prometheus-kube-prometheus-alertmanager-0

# Probar webhook manualmente
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test from curl"}' \
  YOUR_SLACK_WEBHOOK_URL
```

---

## 📚 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

---

## 👤 Autor

**Juan Pablo Alenza**
- GitHub: [@jpalenz77](https://github.com/jpalenz77)
- Proyecto: KC Liberando Productos - Práctica Final

---

## 📝 Licencia

Este proyecto es parte de la práctica final del curso "Liberando Productos" de KeepCoding.