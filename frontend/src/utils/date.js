/**
 * 格式化日期
 * @param {Date|string|number} date - 日期对象
 * @param {string} format - 格式字符串，默认 'yyyy-MM-dd HH:mm:ss'
 * @returns {string} 格式化后的日期字符串
 */
export const formatDate = (date, format = 'yyyy-MM-dd HH:mm:ss') => {
  if (!date) return ''

  const d = new Date(date)

  if (isNaN(d.getTime())) return ''

  const pad = (n) => (n < 10 ? '0' + n : n)

  const formats = {
    'y+': d.getFullYear(),
    'M+': pad(d.getMonth() + 1),
    'd+': pad(d.getDate()),
    'H+': pad(d.getHours()),
    'h+': pad(d.getHours() % 12),
    'm+': pad(d.getMinutes()),
    's+': pad(d.getSeconds()),
    'S+': pad(d.getMilliseconds()),
  }

  let result = format
  for (const key in formats) {
    const regex = new RegExp(key)
    if (regex.test(result)) {
      result = result.replace(regex, (match) => {
        const digits = match.length
        const value = String(formats[key])
        return value.slice(-digits) || value
      })
    }
  }

  return result
}

/**
 * 格式化日期为简短格式
 * @param {Date|string|number} date - 日期对象
 * @returns {string} 格式化后的日期字符串
 */
export const formatDateShort = (date) => {
  return formatDate(date, 'yyyy-MM-dd')
}

/**
 * 格式化日期为长格式
 * @param {Date|string|number} date - 日期对象
 * @returns {string} 格式化后的日期字符串
 */
export const formatDateLong = (date) => {
  return formatDate(date, 'yyyy年MM月dd日 HH:mm:ss')
}

/**
 * 获取相对时间文本
 * @param {Date|string|number} date - 日期对象
 * @returns {string} 相对时间文本
 */
export const getRelativeTime = (date) => {
  const now = new Date()
  const time = new Date(date)
  const diff = now - time

  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour
  const month = 30 * day
  const year = 12 * month

  if (diff < minute) {
    return '刚刚'
  } else if (diff < hour) {
    return Math.floor(diff / minute) + '分钟前'
  } else if (diff < day) {
    return Math.floor(diff / hour) + '小时前'
  } else if (diff < month) {
    return Math.floor(diff / day) + '天前'
  } else if (diff < year) {
    return Math.floor(diff / month) + '个月前'
  } else {
    return Math.floor(diff / year) + '年前'
  }
}

/**
 * 获取今天的日期范围
 * @returns {Array} [开始日期, 结束日期]
 */
export const getTodayRange = () => {
  const today = new Date()
  const start = new Date(today.getFullYear(), today.getMonth(), today.getDate())
  const end = new Date(start.getTime() + 24 * 60 * 60 * 1000 - 1)
  return [start, end]
}

/**
 * 获取昨天的日期范围
 * @returns {Array} [开始日期, 结束日期]
 */
export const getYesterdayRange = () => {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  const start = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate())
  const end = new Date(start.getTime() + 24 * 60 * 60 * 1000 - 1)
  return [start, end]
}

/**
 * 获取本周的日期范围
 * @returns {Array} [开始日期, 结束日期]
 */
export const getWeekRange = () => {
  const today = new Date()
  const firstDay = new Date(today)
  firstDay.setDate(today.getDate() - today.getDay())
  const lastDay = new Date(firstDay)
  lastDay.setDate(firstDay.getDate() + 6)
  lastDay.setHours(23, 59, 59, 999)
  return [firstDay, lastDay]
}

/**
 * 获取本月的日期范围
 * @returns {Array} [开始日期, 结束日期]
 */
export const getMonthRange = () => {
  const today = new Date()
  const firstDay = new Date(today.getFullYear(), today.getMonth(), 1)
  const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0)
  lastDay.setHours(23, 59, 59, 999)
  return [firstDay, lastDay]
}

/**
 * 获取最近N天的日期范围
 * @param {number} days - 天数
 * @returns {Array} [开始日期, 结束日期]
 */
export const getLastDaysRange = (days) => {
  const end = new Date()
  const start = new Date()
  start.setDate(end.getDate() - days + 1)
  start.setHours(0, 0, 0, 0)
  end.setHours(23, 59, 59, 999)
  return [start, end]
}

/**
 * 检查日期是否是今天
 * @param {Date|string|number} date - 日期对象
 * @returns {boolean}
 */
export const isToday = (date) => {
  const today = new Date()
  const checkDate = new Date(date)
  return (
    checkDate.getDate() === today.getDate() &&
    checkDate.getMonth() === today.getMonth() &&
    checkDate.getFullYear() === today.getFullYear()
  )
}

/**
 * 检查日期是否是昨天
 * @param {Date|string|number} date - 日期对象
 * @returns {boolean}
 */
export const isYesterday = (date) => {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  const checkDate = new Date(date)
  return (
    checkDate.getDate() === yesterday.getDate() &&
    checkDate.getMonth() === yesterday.getMonth() &&
    checkDate.getFullYear() === yesterday.getFullYear()
  )
}
