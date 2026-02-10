#!/bin/bash

echo "🔍 系统诊断工具"
echo "========================================="
echo ""

# 检查前端服务
echo "1️⃣  检查前端服务 (Vite)..."
if lsof -i :5173 | grep -q LISTEN; then
    echo "   ✅ 前端服务运行中"
    echo "   地址: http://localhost:5173"
else
    echo "   ❌ 前端服务未运行"
    echo "   需要启动: cd frontend && npm run dev"
fi
echo ""

# 检查后端服务
echo "2️⃣  检查后端服务 (FastAPI)..."
if lsof -i :8000 | grep -q LISTEN; then
    echo "   ✅ 后端服务运行中"
    echo "   地址: http://localhost:8000"
else
    echo "   ❌ 后端服务未运行"
    echo "   需要启动: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
fi
echo ""

# 测试前端连接
echo "3️⃣  测试前端连接..."
if curl -s -m 5 http://localhost:5173 | grep -q "养生商城系统"; then
    echo "   ✅ 前端响应正常"
else
    echo "   ⚠️  前端响应可能有问题"
fi
echo ""

# 测试后端连接
echo "4️⃣  测试后端连接..."
if curl -s -m 5 http://localhost:8000/health | grep -q "ok"; then
    echo "   ✅ 后端响应正常"
else
    echo "   ⚠️  后端响应可能有问题"
fi
echo ""

# 检查Node版本
echo "5️⃣  检查Node.js版本..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "   ✅ Node.js: $NODE_VERSION"
else
    echo "   ❌ Node.js未安装"
fi
echo ""

# 检查Python版本
echo "6️⃣  检查Python版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python未安装"
fi
echo ""

# 检查npm版本
echo "7️⃣  检查npm版本..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "   ✅ npm: $NPM_VERSION"
else
    echo "   ❌ npm未安装"
fi
echo ""

echo "========================================="
echo ""
echo "📍 如果所有检查都是✅，请尝试:"
echo ""
echo "   浏览器访问: http://localhost:5173"
echo "   清除缓存: Ctrl+Shift+Del"
echo "   硬性刷新: Ctrl+Shift+R"
echo "   打开控制台: F12 > Console"
echo ""
echo "❓ 常见问题:"
echo ""
echo "   问题: 浏览器无法连接"
echo "   解决: "
echo "      1. 检查防火墙是否阻止"
echo "      2. 尝试使用 127.0.0.1:5173 而不是 localhost:5173"
echo "      3. 重启浏览器"
echo "      4. 尝试其他浏览器"
echo ""
echo "   问题: 页面空白或显示错误"
echo "   解决: "
echo "      1. 打开F12查看Console标签"
echo "      2. 查看是否有红色错误"
echo "      3. 清除浏览器缓存"
echo "      4. 重新启动Vite服务"
echo ""

echo "✅ 诊断完成！"
