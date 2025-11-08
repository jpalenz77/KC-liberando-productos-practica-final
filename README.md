# KC Liberando Productos - Práctica Final
## Simple Server - Aplicación FastAPI con CI/CD y Monitorización

[![Test](https://github.com/jpalenz77/KC-liberando-productos-practica-final/actions/workflows/test.yml/badge.svg)](https://github.com/jpalenz77/KC-liberando-productos-practica-final/actions/workflows/test.yml)
[![Release](https://github.com/jpalenz77/KC-liberando-productos-practica-final/actions/workflows/release.yml/badge.svg)](https://github.com/jpalenz77/KC-liberando-productos-practica-final/actions/workflows/release.yml)

---

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Guía de Despliegue](#-guía-de-despliegue)
   - [Credenciales y Accesos](#-credenciales-y-accesos)
   - [Requisitos Previos](#requisitos-previos)
   - [Pasos de Instalación](#paso-1-iniciar-minikube)
3. [Endpoints y API](#-endpoints-implementados)
4. [Monitorización](#-monitorización-con-prometheus)
   - [Prometheus](#-monitorización-con-prometheus)
   - [Alertmanager](#-alertas-con-alertmanager)
   - [Dashboard de Grafana](#-dashboard-de-grafana)
5. [Desarrollo y Testing](#-tests-unitarios)
   - [Tests Unitarios](#-tests-unitarios)
   - [CI/CD Pipeline](#-cicd-pipeline)
6. [Configuración](#-helm-chart)
   - [Helm Chart](#-helm-chart)
   - [Troubleshooting](#-troubleshooting)
7. [Recursos Adicionales](#-recursos-adicionales)

---

## 📖 Descripción del Proyecto

Este proyecto implementa una aplicación web simple usando **FastAPI** con los siguientes componentes:

- **Aplicación**: Servidor web con múltiples endpoints
- **Tests**: Cobertura del 93.18% con pytest
- **CI/CD**: GitHub Actions para testing y release
- **Containerización**: Docker image publicada en GHCR
- **Orquestación**: Helm chart para Kubernetes
- **Monitorización**: Prometheus + Grafana + Alertmanager

---

## 🚀 Endpoints Implementados

La aplicación expone los siguientes endpoints:

### 1. **GET /** - Main Endpoint
```shell
curl http://localhost:8081/
```
Response: `{"msg": "Hello World"}`

### 2. **GET /bye** - Nuevo Endpoint (Práctica Final)
```shell
curl http://localhost:8081/bye
```
Response: `{"msg": "Bye Bye"}`

### 3. **GET /health** - Health Check
```shell
curl http://localhost:8081/health
```
Response: `{"health": "ok"}`

### 4. **GET /metrics** - Métricas de Prometheus
```shell
curl http://localhost:8081/metrics
```
Response: métricas en formato Prometheus

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

Los tests cubren todos los endpoints con un **93.18% de cobertura**:

1. ✅ `test_server_initialization()` - Verifica la inicialización del servidor
2. ✅ `test_server_configuration()` - Verifica la configuración del servidor
3. ✅ `test_read_health()` - Verifica endpoint `/health`
4. ✅ `test_read_main()` - Verifica endpoint `/`
5. ✅ `test_read_bye()` - Verifica endpoint `/bye`
6. ✅ `test_metrics()` - Verifica endpoint `/metrics`
7. ✅ `test_multiple_requests()` - Verifica múltiples peticiones
8. ✅ `test_fastapi_app_metadata()` - Verifica metadata de la aplicación
9. ✅ `test_concurrent_requests()` - Verifica peticiones concurrentes
10. ✅ `test_counter_reset()` - Verifica reset de contadores
11. ✅ `test_metrics_content_type()` - Verifica content type de métricas
12. ✅ `test_hypercorn_config()` - Verifica configuración de Hypercorn

### Ejecutar Tests Localmente
```shell
python3 -m venv venv
```

```shell
source venv/bin/activate
```

```shell
pip install -r requirements.txt
```

```shell
pytest --cov --cov-report=term -v
```

```shell
pytest --cov --cov-report=html
```

```shell
open htmlcov/index.html
```

### Resultado Esperado
```
---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                          Stmts   Miss Branch BrPart   Cover
----------------------------------------------------------------
src/__init__.py                   0      0      0      0 100.00%
src/application/__init__.py       0      0      0      0 100.00%
src/application/app.py           36      3      8      0  93.18%
----------------------------------------------------------------
TOTAL                            36      3      8      0  93.18%
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
Ver en GitHub Actions:

```shell
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
```shell
git tag -a v1.0.0 -m "Release version 1.0.0"
```

```shell
git push origin v1.0.0
```

```shell
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
    ├── hpa.yaml            # HorizontalPodAutoscaler
    ├── ingress.yaml        # Ingress (opcional)
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
```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

```shell
helm repo update
```

```shell
helm install simple-server ./helm/simple-server --namespace simple-server --create-namespace --set image.repository=ghcr.io/jpalenz77/kc-liberando-productos-practica-final --set image.tag=latest
```

### Verificar el despliegue
```shell
kubectl get pods -n simple-server
```

```shell
kubectl get svc -n simple-server
```

```shell
kubectl get hpa -n simple-server
```

```shell
kubectl get servicemonitor -n simple-server
```

```shell
kubectl logs -n simple-server -l app.kubernetes.io/name=simple-server -f
```

### Port-forward para acceder
```shell
kubectl port-forward -n simple-server svc/simple-server 8081:8081
```

```shell
curl http://localhost:8081/
```

```shell
curl http://localhost:8081/bye
```

```shell
curl http://localhost:8081/health
```

```shell
curl http://localhost:8081/metrics
```

---

## 📊 Monitorización con Prometheus

### Instalación de kube-prometheus-stack
Crear namespace:
```shell
kubectl create namespace monitoring
```

Instalar Prometheus Operator + Grafana + Alertmanager:
```shell
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --values monitoring/kube-prometheus-stack/values.yaml
```

### Verificar instalación
Ver todos los pods de monitoring:
```shell
kubectl get pods -n monitoring
```

Deberías ver:
- prometheus-operator
- prometheus-prometheus-kube-prometheus-prometheus-0
- alertmanager-prometheus-kube-prometheus-alertmanager-0
- prometheus-grafana-xxx
- prometheus-kube-state-metrics-xxx
- prometheus-prometheus-node-exporter-xxx

### Acceder a Prometheus
```shell
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
```

```shell
open http://localhost:9090
```

### Verificar que las métricas se están recolectando

1. Ve a **Status → Targets**
2. Busca el job `simple-server`
3. Debería estar en estado **UP**

### Queries útiles en Prometheus

Total de requests:
```promql
server_requests_total
```

Rate de requests por segundo:
```promql
rate(server_requests_total[5m])
```

Requests al endpoint /bye:
```promql
bye_requests_total
```

Rate del endpoint /bye:
```promql
rate(bye_requests_total[5m])
```

Comparar todos los endpoints:
```promql
sum by (endpoint) (rate(server_requests_total[5m]))
```

Reinicios de la aplicación:
```promql
kube_pod_container_status_restarts_total{pod=~".*simple-server.*"}
```

---

## 🚨 Alertas con Alertmanager

### Configuración de Slack

⚠️ **IMPORTANTE: Seguridad del Webhook**

El webhook de Slack contiene información sensible y **NUNCA** debe ser commiteado al repositorio.

**Pasos para configurar:**

1. **Crear canal en Slack**: `#josepalenzuela-prometheus-alarms`

2. **Crear Incoming Webhook**:
   - Ve a https://api.slack.com/apps
   - Create New App → From scratch
   - Nombre: "Prometheus Alertmanager"
   - Incoming Webhooks → Activate → Add New Webhook
   - Selecciona tu canal
   - **Copia la URL del webhook**

3. **Instalar Prometheus con el webhook** (usando --set):

**Opción 1: Mediante --set en la línea de comandos (RECOMENDADO)**
```shell
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --values monitoring/kube-prometheus-stack/values.yaml --set alertmanager.config.global.slack_api_url='https://hooks.slack.com/services/YOUR/WEBHOOK/HERE'
```

**Opción 2: Crear archivo secrets.yaml local (NO hacer commit)**

Copiar el ejemplo:
```shell
cp monitoring/kube-prometheus-stack/secrets.example.yaml monitoring/kube-prometheus-stack/secrets.yaml
```

Editar con tu webhook real:
```shell
nano monitoring/kube-prometheus-stack/secrets.yaml
```

Instalar con ambos archivos:
```shell
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --values monitoring/kube-prometheus-stack/values.yaml --values monitoring/kube-prometheus-stack/secrets.yaml
```

**Opción 3: Variable de entorno**

Exportar como variable de entorno:
```shell
export SLACK_WEBHOOK='https://hooks.slack.com/services/YOUR/WEBHOOK/HERE'
```

Usar en helm:
```shell
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --values monitoring/kube-prometheus-stack/values.yaml --set alertmanager.config.global.slack_api_url="$SLACK_WEBHOOK"
```

⚠️ **Recuerda:** El webhook es un secreto. Nunca lo compartas públicamente.

---

## ⚡ Simple Server: Referencia Operacional y Pruebas de Estrés

Este documento sirve como referencia para el monitoreo (Alerts) y como guía para realizar pruebas de rendimiento y escalado (Stress Test) sobre el despliegue de Kubernetes simple-server.

### 🚨 Referencia de Alertas Operacionales

Lista detallada de las reglas de alerta configuradas en nuestro sistema de monitoreo, categorizadas por severidad y tiempo de activación.

| Categoría | Alerta | Condición | Duración | Impacto |
| :---- | :---- | :---- | :---- | :---- |

#### Nivel 1: CRÍTICO (CRITICAL) 🔴

| Alerta | Condición | Retardo (Duración) | Descripción de Impacto |
| :---- | :---- | :---- | :---- |
| SimpleServerDown | Pod caído o no disponible. | **1 minuto** | Interrupción del servicio. Requiere acción inmediata. |
| SimpleServerMemoryLimitReached | Uso de memoria > 90% del límite. | **1 minuto** | Riesgo inminente de OOMKill (eliminación por falta de memoria). |
| SimpleServerConsumingMoreThanRequest | Uso de memoria real > límite de request. | 2 minutos | Saturación de recursos del nodo. |
| SimpleServerCPUThrottlingHigh | Limitación de CPU (Throttling) > 25%. | 5 minutos | Degradación grave del rendimiento. |

#### Nivel 2: ALTO (HIGH) 🟠

| Alerta | Condición | Retardo (Duración) | Descripción de Impacto |
| :---- | :---- | :---- | :---- |
| SimpleServerPodRestarting | El Pod en ciclo de reinicios. | 5 minutos | Inestabilidad del servicio. |
| SimpleServerCPUConsumingMoreThanRequest | Uso de CPU real > límite de request. | 2 minutos | Consumo ineficiente, potencial latencia. |
| SimpleServerHighRequestRate | Tasa de peticiones > 100 req/s. | 5 minutos | Alerta de tráfico elevado. |
| SimpleServerNoRequests | No se han recibido peticiones. | 10 minutos | Indicio de problema en el balanceador. |

### 💥 Guía de Stress Test con NodeWrecker

Este procedimiento utiliza la herramienta **NodeWrecker** para generar una carga artificial intensa (CPU y Memoria) dentro de un pod. El objetivo es validar el **Horizontal Pod Autoscaler (HPA)**.

#### 📝 Requisitos
- Acceso kubectl configurado al clúster.
- El Pod debe tener permisos para ejecutar apk y go build.

#### Paso 1: Identificar el Pod Target
Obtén el nombre del pod de simple-server.
```shell
kubectl get pods -n simple-server
```
Ejemplo de salida: `simple-server-b87696dcc-gzzzz`

#### Paso 2: Acceder al Contenedor 🚪
Abre una sesión interactiva. Reemplaza "simple-server-xxxxxxxx-yyyyy" con el nombre del pod obtenido en el paso anterior:
```shell
kubectl -n simple-server exec --stdin --tty simple-server-xxxxxxxx-yyyyy -c simple-server -- /bin/sh
```

#### Paso 3: Instalar Dependencias 🛠️
Dentro del pod, instala las herramientas necesarias (git y go).
```shell
apk update
```

```shell
apk add git go
```

#### Paso 4: Clonar y Compilar NodeWrecker
Descarga y genera el binario ejecutable (extress):
```shell
git clone https://github.com/jaeg/NodeWrecker.git
```

```shell
cd NodeWrecker
```

```shell
go build -o extress main.go
```

#### Paso 5: Ejecutar la Prueba de Estrés 🔥
Inicia la carga intensiva sobre el Pod.
```bash
./extress -abuse-memory -escalate -max-duration 10000000
```
**Consejo:** Detén la prueba manualmente en cualquier momento con `Ctrl + C`.

#### Paso 6: Monitorizar el HPA 📈
**En una terminal NUEVA (fuera del pod)**, observa el comportamiento del autoscaler.
```bash
kubectl -n simple-server get hpa -w
```

#### Paso 7: Observar el Escalado 🚀
**En otra terminal NUEVA**, sigue la creación de réplicas.
```bash
kubectl -n simple-server get pods -w
```

#### Paso 8: Finalizar y Desescalar 🧹
Detén la ejecución de extress (`Ctrl + C`) en la sesión del pod. El HPA iniciará el *downscaling*.

### Acceder a Alertmanager
```shell
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-alertmanager 9093:9093
```

```shell
open http://localhost:9093
```

---

## 📈 Dashboard de Grafana

### Acceder a Grafana
```shell
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

```shell
open http://localhost:3000
```

Obtener la contraseña de administrador:
```shell
kubectl get secret prometheus-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

> 💡 **Importante**: Guarda esta contraseña en un lugar seguro, la necesitarás para acceder al dashboard

### Importar Dashboard

**Opción 1: Mediante ConfigMap (Automático)**

Aplicar el ConfigMap:
```shell
kubectl apply -f monitoring/grafana/simple-server-dashboard-configmap.yaml
```

El dashboard aparecerá automáticamente en Grafana.

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
```shell
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

### 🔑 Credenciales y Accesos

#### Grafana
- **Usuario**: admin
- **Obtener contraseña**:
  ```bash
  kubectl get secret prometheus-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
  ```
  > 💡 **Importante**: Guarda esta contraseña en un lugar seguro

#### URLs de Acceso (después del despliegue)
- **Aplicación**: http://localhost:8081
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
- **Alertmanager**: http://localhost:9093

### Requisitos Previos

- Docker
- Kubernetes (Minikube, Kind, K3s, o cluster real)
- kubectl configurado
- Helm 3.x
- Git

### Paso 1: Iniciar Minikube
```shell
minikube start --cpus=4 --memory=8192 --driver=docker
```
Iniciar minikube con los recursos necesarios:
```shell
minikube start --cpus=4 --memory=8192 --driver=docker
```

Habilitar el addon metrics-server:
```shell
minikube addons enable metrics-server
```

Verificar que el nodo está funcionando:
```shell
kubectl get nodes
```

```shell
minikube addons enable metrics-server
```

```shell
kubectl get nodes
```

### Paso 2: Instalar Prometheus Stack
```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --values monitoring/kube-prometheus-stack/values.yaml \
  --set alertmanager.config.global.slack_api_url='https://hooks.slack.com/services/XXX/YYY/ZZZ'
kubectl get pods -n monitoring -w
```

### Paso 3: Desplegar Simple Server
```shell
kubectl create namespace simple-server
helm install simple-server ./helm/simple-server --namespace simple-server --set image.repository=ghcr.io/jpalenz77/kc-liberando-productos-practica-final --set image.tag=latest --set metrics.enabled=true
kubectl get pods -n simple-server
kubectl get svc -n simple-server
kubectl get servicemonitor -n simple-server
```

### Paso 4: Aplicar Dashboard de Grafana
```shell
kubectl apply -f monitoring/grafana/simple-server-dashboard-configmap.yaml
kubectl get configmap -n monitoring simple-server-dashboard
```

### Paso 5: Acceder a las Interfaces
```shell
kubectl port-forward -n simple-server svc/simple-server 8081:8081
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-alertmanager 9093:9093
```

**URLs:**
- Aplicación: http://localhost:8081
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin / prom-operator)
- Alertmanager: http://localhost:9093

### Paso 6: Verificar que Todo Funciona
```shell
curl http://localhost:8081/
curl http://localhost:8081/bye
curl http://localhost:8081/health
curl http://localhost:8081/metrics
kubectl scale deployment simple-server -n simple-server --replicas=0
kubectl scale deployment simple-server -n simple-server --replicas=2
```

---

## 🔍 Troubleshooting

### Problema: Tests fallan localmente
```shell
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest --cov -v
```

### Problema: Docker image no se construye
```shell
docker build -t simple-server:test .
docker build -t simple-server:test . --progress=plain
```

### Problema: Pods no inician en Kubernetes
```shell
kubectl describe pod -n simple-server <pod-name>
kubectl logs -n simple-server <pod-name>
kubectl get events -n simple-server --sort-by='.lastTimestamp'
```

### Problema: Prometheus no encuentra targets
```shell
kubectl get servicemonitor -n simple-server -o yaml
kubectl get svc -n simple-server -o yaml
kubectl logs -n monitoring prometheus-prometheus-kube-prometheus-prometheus-0
```

### Problema: Dashboard no aparece en Grafana
```shell
kubectl get configmap -n monitoring simple-server-dashboard
kubectl get configmap -n monitoring simple-server-dashboard -o yaml | grep labels -A 5
kubectl rollout restart deployment -n monitoring prometheus-grafana
```

### Problema: Alertas no llegan a Slack
```shell
kubectl get secret -n monitoring alertmanager-prometheus-kube-prometheus-alertmanager -o yaml
kubectl logs -n monitoring alertmanager-prometheus-kube-prometheus-alertmanager-0
curl -X POST -H 'Content-type: application/json' --data '{"text":"Test from curl"}' YOUR_SLACK_WEBHOOK_URL
```

---

## 📚 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)