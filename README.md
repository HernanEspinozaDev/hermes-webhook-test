# Lúmina Plata

Tienda web estática de demostración para una boutique de joyas de plata. El sitio está hecho con HTML y CSS, sin backend ni dependencias de ejecución: una base sencilla para probar el flujo de trabajo de Kanban, pull requests, revisión y notificaciones de Hermes.

## Ver localmente

Abre `index.html` directamente en el navegador. Los estilos y recursos gráficos están guardados localmente en el repositorio.

## Validar

Requiere Node.js 22 o posterior, sin instalar paquetes:

```bash
node --test
```

La suite verifica el contenido principal, los enlaces internos, los recursos locales y los estilos responsivos. GitHub Actions ejecuta las mismas pruebas en cada pull request.

> Marca, productos, descripciones y precios son contenido ficticio de demostración; no hay compra ni procesamiento de pagos.
