# Импорт данных

Импорт данных из файлов на сайте https://eddb.io/api в базу данных

## Описание

Загрузка данных из JSON в базу данных PostgresSQL

1. systems.csv - файл в формате csv, на лету заполняются следующие структуры:
  * governments - справочник типов правлений
  * allegiances - справочник
  * states - справочник состояний
  * securitys - справочник безопасности
  * economys - справочник экономик
  * power_states - справочник состояний сил
  * reserve_types - справочник резервных типов
