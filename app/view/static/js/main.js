// Основной модуль приложения
const App = (() => {
    // Конфигурация
    const config = {
        apiBaseUrl: '/api',
        wsBaseUrl: ws://${window.location.host}/ws,
        updateInterval: 2000,
        notificationTimeout: 5000
    }

    // Элементы DOM
    const elements = {
        predictionForm: document.getElementById('predictionForm'),
        inputDataTextarea: document.getElementById('input_data'),
        resultContainer: document.getElementById('resultContainer'),
        taskStatus: document.getElementById('taskStatus'),
        predictionResult: document.getElementById('predictionResult'),
        balanceElement: document.querySelector('.balance-amount'),
        notificationContainer: document.getElementById('notificationContainer')
    }

    // Инициализация приложения
    function init() {
        setupEventListeners()
        connectWebSocket()
        updateBalancePeriodically()
    }

    // Настройка обработчиков событий
    function setupEventListeners() {
        if (elements.predictionForm) {
            elements.predictionForm.addEventListener('submit', handlePredictionSubmit)
        }
    }

    // Обработчик отправки формы предсказания
    async function handlePredictionSubmit(e) {
        e.preventDefault()

        const submitButton = e.target.querySelector('button[type="submit"]')
        submitButton.disabled = true
        submitButton.textContent = 'Отправка...'

        try {
            const inputData = parseInputData()
            const response = await sendPredictionRequest(inputData)
            handlePredictionResponse(response)
        } catch (error) {
            showNotification(error.message, 'error')
        } finally {
            submitButton.disabled = false
            submitButton.textContent = 'Отправить'
        }
    }

    // Парсинг входных данных
    function parseInputData() {
        try {
            return JSON.parse(elements.inputDataTextarea.value)
        } catch (error) {
            throw new Error('Неверный формат JSON данных')
        }
    }

    // Отправка запроса на создание предсказания
    async function sendPredictionRequest(inputData) {
        const response = await fetch(`${config.apiBaseUrl}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': Bearer ${getAuthToken()}
            },
            body: JSON.stringify({ input_data: inputData })
        })

        if (!response.ok) {
            const error = await response.json()
            throw new Error(error.detail || 'Ошибка сервера')
        }

        return response.json()
    }

    // Обработка ответа от API
    function handlePredictionResponse(response) {
        showNotification('Задача успешно создана', 'success')
        elements.resultContainer.classList.remove('hidden')
        monitorTaskStatus(response.task_id)
        updateBalance()
    }

    // Мониторинг статуса задачи
    async function monitorTaskStatus(taskId) {
        const intervalId = setInterval(async () => {
            try {
                const task = await fetchTaskStatus(taskId)
                updateTaskStatusUI(task)

                if (task.status === 'completed' || task.status === 'failed') {
                    clearInterval(intervalId)
                    if (task.status === 'completed') {
                        updateBalance()
                    }
                }
            } catch (error) {
                clearInterval(intervalId)
                showNotification(error.message, 'error')
            }
        }, config.updateInterval)
    }

    // Получение статуса задачи
    async function fetchTaskStatus(taskId) {
        const response = await fetch(`${config.apiBaseUrl}/tasks/${taskId}`, {
            headers: {
                'Authorization': Bearer ${getAuthToken()}
            }
        })

        if (!response.ok) {
            throw new Error('Не удалось получить статус задачи')
        }

        return response.json()
    }

    // Обновление UI статуса задачи
    function updateTaskStatusUI(task) {
        elements.taskStatus.textContent = task.status
        elements.taskStatus.className = status-${task.status}

        if (task.result) {
            elements.predictionResult.innerHTML =
                <pre>${JSON.stringify(task.result, null, 2)}</pre>
        }
    }

    // Обновление баланса
    async function updateBalance() {
        try {
            const response = await fetch(`${config.apiBaseUrl}/balance`, {
                headers: {
                    'Authorization': Bearer ${getAuthToken()}
                }
            })

            if (response.ok) {
                const data = await response.json()
                elements.balanceElement.textContent = ${data.balance} $
            }
        } catch (error) {
            console.error('Ошибка обновления баланса:', error)
        }
    }

    // Периодическое обновление баланса
    function updateBalancePeriodically() {
        setInterval(updateBalance, 30000) // Каждые 30 секунд
        updateBalance() // Первоначальное обновление
    }

    // WebSocket подключение
    function connectWebSocket() {
        const socket = new WebSocket(config.wsBaseUrl)

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data)
            if (message.type === 'balance_update') {
                elements.balanceElement.textContent = ${message.balance} $
            }
        }

        socket.onerror = (error) => {
            console.error('WebSocket error:', error)
        }
    }

    // Отображение уведомлений
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div')
        notification.className = notification notification-${type}
        notification.textContent = message

        elements.notificationContainer.appendChild(notification)

        setTimeout(() => {
            notification.remove()
        }, config.notificationTimeout)
    }

    // Получение токена аутентификации
    function getAuthToken() {
        return localStorage.getItem('authToken') || ''
    }

    // Публичные методы
    return {
        init
    }
})()

// Инициализация приложения после загрузки DOM
document.addEventListener('DOMContentLoaded', App.init)
