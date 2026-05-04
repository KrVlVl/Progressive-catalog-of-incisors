from fastapi import APIRouter, Response

router = APIRouter(tags=["styles"])

@router.get("/style.css")
async def get_style():
    css = """
/* ========================================
   Сервис подбора режущих пластин
   Финальная версия: контрастные цвета
   Версия: 1.0
======================================== */

/* ---------- Сброс стилей ---------- */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* ---------- Основные стили (тёплый фон) ---------- */
html, body {
    height: 100%;
}

body {
    font-family: 'Segoe UI', 'Segoe UI Semibold', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD700 100%);
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* ---------- Контейнер ---------- */
.container {
    flex: 1 0 auto;
    max-width: 1400px;
    margin: 2rem auto;
    padding: 0 20px;
    width: 100%;
}

/* ---------- Навигация ---------- */
.navbar {
    background: linear-gradient(to bottom, #E85D04 0%, #DC2F02 100%);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    padding: 0.8rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
    position: sticky;
    top: 0;
    z-index: 1000;
    border-bottom: 2px solid #FFB703;
}

.nav-brand h1 {
    color: #FFF;
    font-size: 1.5rem;
    font-weight: 600;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.nav-links {
    display: flex;
    gap: 10px;
}

.nav-links a {
    color: white;
    text-decoration: none;
    padding: 8px 20px;
    border-radius: 25px;
    transition: all 0.3s ease;
    font-weight: 500;
    font-size: 14px;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.nav-links a:hover {
    background: #FFB703;
    color: #DC2F02;
    transform: translateY(-2px);
    border-color: #FFD700;
    box-shadow: 0 5px 15px rgba(255, 183, 3, 0.4);
}

/* ---------- Карточки ---------- */
.card {
    background: linear-gradient(135deg, #FFF8F0 0%, #FFEFD5 100%);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 25px;
    border: 1px solid #FFB703;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    border-color: #FF6B35;
}

/* ---------- Заголовки (контрастные) ---------- */
h1 {
    font-size: 2.3rem;
    margin-bottom: 1rem;
    color: #1A252F;
    font-weight: 700;
    text-shadow: none;
}

h2 {
    color: #1A5276;
    margin-bottom: 1.3rem;
    font-size: 1.7rem;
    border-left: 5px solid #FF6B35;
    padding-left: 15px;
    font-weight: 600;
}

h3 {
    color: #2C3E50;
    margin-bottom: 1rem;
    font-size: 1.3rem;
    font-weight: 600;
}

/* ---------- Формы ---------- */
.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #1A5276;
    font-size: 14px;
}

input, select, textarea {
    width: 100%;
    padding: 12px 15px;
    border: 2px solid #FFD700;
    border-radius: 12px;
    background: #FFFFFF;
    font-size: 14px;
    font-family: inherit;
    transition: all 0.3s ease;
    color: #2C3E50;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #FF6B35;
    box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.2);
    background: #FFFDF9;
}

/* ---------- Кнопки ---------- */
button, .btn {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 10px 28px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
    margin: 5px;
    box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

button:hover, .btn:hover {
    background: linear-gradient(135deg, #FF8C42 0%, #FFB703 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4);
}

button:active, .btn:active {
    transform: translateY(1px);
}

.btn-danger {
    background: linear-gradient(135deg, #FF4757 0%, #FF6B81 100%);
}

.btn-success {
    background: linear-gradient(135deg, #28A745 0%, #34CE57 100%);
}

/* ---------- Алерты ---------- */
.alert {
    padding: 15px 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    animation: slideIn 0.4s ease;
}

.alert-success {
    background: linear-gradient(135deg, #D4EDDA 0%, #C3E6CB 100%);
    color: #155724;
    border-left: 5px solid #28A745;
}

.alert-error {
    background: linear-gradient(135deg, #F8D7DA 0%, #F5C6CB 100%);
    color: #721C24;
    border-left: 5px solid #FF4757;
}

.alert-icon {
    font-size: 20px;
}

@keyframes slideIn {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* ---------- Элементы пластин ---------- */
.plate-item, .recommendation-item {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF9F0 100%);
    padding: 20px;
    margin: 15px 0;
    border-radius: 15px;
    border-left: 5px solid #FF6B35;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    color: #2C3E50;
}

.plate-item:hover, .recommendation-item:hover {
    transform: translateX(8px);
    box-shadow: 0 5px 20px rgba(255, 107, 53, 0.2);
    border-left-color: #FFB703;
}

.recommendation-item {
    background: linear-gradient(135deg, #FFF5E8 0%, #FFEFD5 100%);
    border-left-color: #28A745;
}

.score {
    font-size: 26px;
    font-weight: bold;
    color: #28A745;
    display: inline-block;
    padding: 5px 15px;
    background: linear-gradient(135deg, #D4EDDA 0%, #C3E6CB 100%);
    border-radius: 30px;
}

/* ---------- Таблицы ---------- */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

th {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    color: white;
    padding: 12px 15px;
    text-align: left;
    font-weight: 600;
    font-size: 14px;
}

td {
    padding: 10px 15px;
    border-bottom: 1px solid #FFE0B5;
    background: #FFFDF9;
    color: #2C3E50;
}

tr:hover td {
    background: #FFF5E8;
}

/* ---------- Сетки ---------- */
.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 25px;
    margin-top: 20px;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
}

/* ---------- Футер ---------- */
.footer {
    flex-shrink: 0;
    background: linear-gradient(135deg, #DC2F02 0%, #E85D04 100%);
    color: #FFE0B5;
    text-align: center;
    padding: 15px;
    width: 100%;
    margin-top: auto;
    border-top: 2px solid #FFB703;
    font-size: 12px;
}

.footer-content {
    max-width: 1200px;
    margin: 0 auto;
}

.footer-links {
    margin-top: 8px;
    font-size: 11px;
}

.footer-links a {
    color: #FFD700;
    text-decoration: none;
    margin: 0 5px;
    transition: all 0.3s ease;
}

.footer-links a:hover {
    text-decoration: underline;
    color: #FFFFFF;
}

/* ---------- Badge ---------- */
.badge {
    display: inline-block;
    padding: 4px 12px;
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    color: white;
    border-radius: 20px;
    font-size: 11px;
    margin-left: 10px;
}

/* ---------- Код ---------- */
code {
    background: #FFEFD5;
    padding: 3px 8px;
    border-radius: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    color: #DC2F02;
}

/* ---------- Главная страница ---------- */
.hero-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-top: 30px;
}

.hero-buttons .btn {
    font-size: 16px;
    padding: 12px 35px;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.feature-card {
    padding: 25px;
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF8F0 100%);
    text-align: center;
    border-radius: 20px;
    transition: all 0.3s ease;
    border: 1px solid #FFD700;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: #FF6B35;
    box-shadow: 0 10px 30px rgba(255, 107, 53, 0.2);
}

.feature-icon {
    font-size: 50px;
    margin-bottom: 15px;
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 10px;
    color: #1A5276;
}

.feature-desc {
    font-size: 13px;
    color: #34495E;
}

/* ---------- Анимации ---------- */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.5s ease;
}

/* ---------- Утилиты ---------- */
.text-center {
    text-align: center;
}

.text-right {
    text-align: right;
}

.mt-1 { margin-top: 10px; }
.mt-2 { margin-top: 20px; }
.mt-3 { margin-top: 30px; }
.mb-1 { margin-bottom: 10px; }
.mb-2 { margin-bottom: 20px; }
.mb-3 { margin-bottom: 30px; }

.hidden {
    display: none;
}

/* ---------- Скроллбар ---------- */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-track {
    background: #FFEFD5;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #FF8C42 0%, #FFB703 100%);
}
    """
    return Response(content=css, media_type="text/css")