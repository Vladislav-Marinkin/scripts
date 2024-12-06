#!/bin/bash

# Переменные
NODE_EXPORTER_VERSION="1.6.1"
DOWNLOAD_URL="https://github.com/prometheus/node_exporter/releases/download/v${NODE_EXPORTER_VERSION}/node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz"
INSTALL_DIR="/usr/local/bin"
SERVICE_FILE="/etc/systemd/system/node-exporter.service"

# Проверка выполнения от root
if [ "$EUID" -ne 0 ]; then
  echo "Пожалуйста, запустите скрипт от имени root."
  exit 1
fi

# Функция для установки Node Exporter
install_node_exporter() {
  echo "Установка Node Exporter..."

  # Скачивание и установка Node Exporter
  echo "Скачиваем Node Exporter..."
  wget -q $DOWNLOAD_URL -O /tmp/node_exporter.tar.gz
  if [ $? -ne 0 ]; then
    echo "Ошибка при загрузке Node Exporter."
    exit 1
  fi

  echo "Распаковываем Node Exporter..."
  tar -xzf /tmp/node_exporter.tar.gz -C /tmp
  cp /tmp/node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64/node_exporter $INSTALL_DIR/

  # Проверка установки
  if ! command -v node_exporter &> /dev/null; then
    echo "Node Exporter не установлен."
    exit 1
  fi
  echo "Node Exporter успешно установлен."

  # Создание системного сервиса
  echo "Создаём системный сервис для Node Exporter..."
  cat <<EOL > $SERVICE_FILE
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=nobody
ExecStart=${INSTALL_DIR}/node_exporter --web.listen-address="0.0.0.0:9100"
Restart=always

[Install]
WantedBy=default.target
EOL

  # Перезагрузка Systemd и запуск сервиса
  echo "Перезагружаем systemd и запускаем Node Exporter..."
  systemctl daemon-reload
  systemctl enable node-exporter
  systemctl start node-exporter

  # Проверка статуса сервиса
  if systemctl is-active --quiet node-exporter; then
    echo "Node Exporter успешно запущен и работает."
    echo "Вы можете проверить метрики по адресу: http://<ваш IP>:9100/metrics"
  else
    echo "Не удалось запустить Node Exporter. Проверьте журнал: journalctl -u node-exporter"
  fi

  # Удаление временных файлов
  echo "Чистим временные файлы..."
  rm -rf /tmp/node_exporter*
  echo "Установка завершена."
}

# Функция для удаления Node Exporter
uninstall_node_exporter() {
  echo "Удаление Node Exporter..."

  # Остановка и отключение службы
  if systemctl is-active --quiet node-exporter; then
    echo "Останавливаем Node Exporter..."
    systemctl stop node-exporter
  fi
  echo "Отключаем Node Exporter..."
  systemctl disable node-exporter

  # Удаление системного сервиса
  echo "Удаляем файл службы Node Exporter..."
  rm -f $SERVICE_FILE
  systemctl daemon-reload

  # Удаление бинарного файла
  echo "Удаляем бинарный файл Node Exporter..."
  rm -f ${INSTALL_DIR}/node_exporter

  echo "Node Exporter успешно удалён."
}

# Главное меню
echo "Node Exporter Installer"
echo "Выберите действие:"
echo "1) Установить Node Exporter"
echo "2) Удалить Node Exporter"
echo "3) Выйти"

read -p "Введите номер действия: " action
case $action in
  1)
    install_node_exporter
    ;;
  2)
    uninstall_node_exporter
    ;;
  3)
    echo "Выход."
    exit 0
    ;;
  *)
    echo "Некорректный ввод. Попробуйте снова."
    exit 1
    ;;
esac