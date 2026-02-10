/**
 * 工具函数
 */

/**
 * 格式化日期
 * @param {Date|string|number} date - 日期对象或时间戳
 * @param {string} format - 格式化字符串，默认 'YYYY-MM-DD HH:mm:ss'
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return '';

  if (typeof date === 'number' || typeof date === 'string') {
    date = new Date(parseInt(date));
  }

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
}

/**
 * 格式化金额
 * @param {number} amount - 金额
 * @param {number} fixed - 小数位数
 */
export function formatMoney(amount, fixed = 2) {
  if (typeof amount !== 'number') {
    return '¥0.00';
  }
  return `¥${amount.toFixed(fixed)}`;
}

/**
 * 防抖函数
 * @param {function} fn - 要执行的函数
 * @param {number} wait - 等待时间（毫秒）
 */
export function debounce(fn, wait = 300) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      fn.apply(this, args);
    }, wait);
  };
}

/**
 * 节流函数
 * @param {function} fn - 要执行的函数
 * @param {number} wait - 等待时间（毫秒）
 */
export function throttle(fn, wait = 300) {
  let timeout;
  return function (...args) {
    if (!timeout) {
      timeout = setTimeout(() => {
        fn.apply(this, args);
        timeout = null;
      }, wait);
    }
  };
}

/**
 * 显示加载提示
 * @param {string} title - 提示文字
 */
export function showLoading(title = '加载中...') {
  wx.showLoading({
    title: title,
    mask: true,
  });
}

/**
 * 隐藏加载提示
 */
export function hideLoading() {
  wx.hideLoading();
}

/**
 * 显示提示框
 * @param {string} title - 标题
 * @param {string} content - 内容
 */
export function showModal(title, content) {
  return new Promise((resolve) => {
    wx.showModal({
      title: title,
      content: content,
      success: (res) => {
        resolve(res.confirm);
      },
    });
  });
}

/**
 * 显示消息提示
 * @param {string} message - 消息内容
 * @param {string} type - 类型：success/error/loading
 */
export function showMessage(message, type = 'success') {
  wx.showToast({
    title: message,
    icon: type === 'loading' ? 'loading' : type === 'error' ? 'error' : 'success',
    duration: 2000,
  });
}

/**
 * 本地存储
 */
export const storage = {
  set(key, value) {
    wx.setStorageSync(key, value);
  },

  get(key) {
    return wx.getStorageSync(key);
  },

  remove(key) {
    wx.removeStorageSync(key);
  },

  clear() {
    wx.clearStorageSync();
  },
};

/**
 * 将参数对象转换为查询字符串
 */
export function toQueryString(obj) {
  return Object.keys(obj)
    .map((key) => `${encodeURIComponent(key)}=${encodeURIComponent(obj[key])}`)
    .join('&');
}

export default {
  formatDate,
  formatMoney,
  debounce,
  throttle,
  showLoading,
  hideLoading,
  showModal,
  showMessage,
  storage,
  toQueryString,
};
