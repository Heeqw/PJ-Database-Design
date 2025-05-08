import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_merchant_login():
    """测试商家登录API"""
    url = f"{BASE_URL}/merchants/login/"
    # 尝试所有可能的商家用户名
    usernames = ["校园餐厅".replace(' ', '_').lower(),
                "快乐食堂".replace(' ', '_').lower(),
                "美味小厨".replace(' ', '_').lower()]

    for username in usernames:
        data = {
            "username": username,
            "password": "merchant123"
        }
        response = requests.post(url, json=data)
        print(f"商家 '{username}' 登录响应状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"商家登录成功: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            return response.json().get('token')
        else:
            print(f"商家登录失败: {response.text}")

    return None

def test_merchant_info(token):
    """测试获取商家信息API"""
    url = f"{BASE_URL}/merchants/info/"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    print(f"获取商家信息响应状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"获取商家信息成功: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"获取商家信息失败: {response.text}")

def test_search_merchants():
    """测试搜索商家API"""
    url = f"{BASE_URL}/merchants/search/"
    response = requests.get(url)
    print(f"搜索商家响应状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"搜索商家成功: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"搜索商家失败: {response.text}")

def test_user_login():
    """测试用户登录API"""
    url = f"{BASE_URL}/users/login/"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(url, json=data)
    print(f"用户登录响应状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"用户登录成功: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.json().get('token')
    else:
        print(f"用户登录失败: {response.text}")
        return None

def main():
    print("开始测试API...")

    # 测试搜索商家
    print("\n=== 测试搜索商家 ===")
    test_search_merchants()

    # 测试商家登录
    print("\n=== 测试商家登录 ===")
    merchant_token = test_merchant_login()

    # 如果商家登录成功，测试获取商家信息
    if merchant_token:
        print("\n=== 测试获取商家信息 ===")
        test_merchant_info(merchant_token)

    # 测试用户登录
    print("\n=== 测试用户登录 ===")
    user_token = test_user_login()

    print("\n测试完成!")

if __name__ == "__main__":
    main()
