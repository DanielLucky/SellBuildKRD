run:
	docker run -d -p 80:8000 --name SellBuildKRD --rm 65fa27e5f9b2

run-dev:
	docker run -d -p 80:8000 --name SellBuildKRD -v "/home/dl/PycharmProjects/SellBuildKRD:/app" --rm 65fa27e5f9b2

run-mysql:
	docker run --name some-mysql -v db:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root_pass -e MYSQL_DATABASE=django -e MYSQL_USER=django -e MYSQL_PASSWORD=django_pass --rm  mysql


stop:
	docker stop SellBuildKRD