# Guía rápida (How-to) para administradores y desarrolladores

Consultar logs desde Django shell

```py
from core.models import AuditLog

# Últimas 10 entradas
AuditLog.objects.all().order_by('-timestamp')[:10]

# Filtrar por acción
AuditLog.objects.filter(action='delete').order_by('-timestamp')[:50]

# Filtrar por usuario
AuditLog.objects.filter(actor__username='admin')
```

Exportar a CSV (ejemplo rápido)

```py
import csv
from core.models import AuditLog

qs = AuditLog.objects.all().order_by('-timestamp')[:1000]
with open('audit_export.csv','w',newline='',encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['timestamp','actor','action','object','object_pk','ip','path'])
    for a in qs:
        w.writerow([a.timestamp,a.actor,a.action,a.object_repr,a.object_pk,a.ip_address,a.path])
```

Restauración / Backups

- Las entradas de auditoría deben incluirse en backups regulares. Para SQLite, hacer copia del archivo `src/db.sqlite3`.
- En entornos con base de datos gestionada, usar backups automáticos del proveedor.

Administración en la UI

- `AuditLog` está registrado en el admin como solo lectura. Solo superusuarios deberían tener acceso.
