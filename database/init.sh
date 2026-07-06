#!/bin/bash
set -e

echo "Waiting for SQL Server to be online..."
until /opt/mssql-tools/bin/sqlcmd -S db -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT 1" &>/dev/null; do
    echo "SQL Server is starting up..."
    sleep 2
done

echo "SQL Server is ready. Running schema script..."
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P "$MSSQL_SA_PASSWORD" -i /database/neu_admission.sql

echo "Running views script..."
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P "$MSSQL_SA_PASSWORD" -i /database/vw_phan_tich_tuyensinh.sql

echo "Running data seeding script (this might take a minute)..."
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P "$MSSQL_SA_PASSWORD" -i /database/DuLieuTuyenSinh_SQLServer.sql

echo "Database initialization completed successfully!"
