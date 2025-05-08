# PJ_Database_Design

#### 介绍
复旦大学24春<数据库设计>课程校园点餐系统PJ项目代码存放仓库

#### 软件架构
前后端分离开发，使用Django REST framework和 Vue3 开发完成

#### 安装教程

1. 直接clone即可

#### 使用说明（传统方式）

1. settings.py中部署好对应的数据库与数据库用户等相关信息
2. python manage.py createsuperuser 创建管理员超级用户用于访问管理员界面
3. clone 仓库后进入food_ordering_system文件夹python manage.py runserver 运行Python Django REST framework 后端框架
4. 进入/food_ordering_system/frontend文件夹 npm install 安装需要的modules
5. npm run serve 运行Vue框架构建前端

#### Docker 部署说明

本项目已经容器化，提供了三种Docker Compose配置文件：

##### 1. 默认配置 (docker-compose.yml)

使用DockerHub上的预构建镜像。

```bash
# 启动应用
docker-compose up -d

# 停止应用
docker-compose down
```

##### 2. 本地开发配置 (docker-compose.local.yml)

本地构建镜像并挂载源代码目录，适合开发使用。

```bash
# 使用本地开发配置启动应用
docker-compose -f docker-compose.local.yml up -d

# 停止应用
docker-compose -f docker-compose.local.yml down
```

##### 3. 生产环境配置 (docker-compose.prod.yml)

使用DockerHub上的预构建镜像，针对生产环境优化。

```bash
# 使用生产配置启动应用
docker-compose -f docker-compose.prod.yml up -d

# 停止应用
docker-compose -f docker-compose.prod.yml down
```

#### 访问应用

- 前端: http://localhost:8080
- 后端API: http://localhost:8000
- 数据库: localhost:13306 (外部连接)

#### Docker 镜像

本项目使用的Docker镜像已发布到DockerHub：

- 后端: [catherineheqw/food-ordering-backend](https://hub.docker.com/r/catherineheqw/food-ordering-backend)
- 前端: [catherineheqw/food-ordering-frontend](https://hub.docker.com/r/catherineheqw/food-ordering-frontend)
- 数据库: [catherineheqw/food-ordering-db](https://hub.docker.com/r/catherineheqw/food-ordering-db)

#### 构建和推送Docker镜像

如果需要更新Docker镜像，请按照以下步骤操作：

```bash
# 构建镜像
docker-compose -f docker-compose.local.yml build

# 标记镜像
docker tag pj-database-design-backend catherineheqw/food-ordering-backend:latest
docker tag pj-database-design-frontend catherineheqw/food-ordering-frontend:latest
docker tag mysql:8.0 catherineheqw/food-ordering-db:latest

# 推送镜像到DockerHub
docker push catherineheqw/food-ordering-backend:latest
docker push catherineheqw/food-ordering-frontend:latest
docker push catherineheqw/food-ordering-db:latest
```

#### 数据初始化

应用启动时会自动初始化数据库，包括：
- 示例商家
- 示例菜品
- 过敏原信息
- 管理员用户 (用户名: admin, 密码: admin)

#### 测试API

可以使用提供的测试脚本测试API：

```bash
python test_api.py
```

该脚本测试各种API端点，包括：
- 商家搜索
- 商家登录
- 用户登录
- 获取商家信息

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request



