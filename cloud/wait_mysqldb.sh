set -e
echo -n "waiting for TCP connection to $host:$port..."

while ! exec 6<>/dev/tcp/$DB_DEFAULT_HOST/3306
do
  echo -n .
  sleep 1
done

echo '=====mysql is connected====='
