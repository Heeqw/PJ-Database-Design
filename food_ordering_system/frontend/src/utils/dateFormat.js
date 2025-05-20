/**
 * 格式化日期为 YYYY-MM-DD 格式
 * @param {Date|string} date - 日期对象或日期字符串
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date) {
  if (!date) return '';
  
  const d = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(d.getTime())) return '';
  
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  
  return `${year}-${month}-${day}`;
}

/**
 * 格式化时间为 HH:MM:SS 格式
 * @param {string} time - 时间字符串
 * @returns {string} 格式化后的时间字符串
 */
export function formatTime(time) {
  if (!time) return '';
  return time.substring(0, 8); // 假设时间格式为 HH:MM:SS
}

/**
 * 格式化日期时间为 YYYY-MM-DD HH:MM:SS 格式
 * @param {string} dateTime - ISO格式的日期时间字符串
 * @returns {string} 格式化后的日期时间字符串
 */
export function formatDateTime(dateTime) {
  if (!dateTime) return '';
  
  const d = new Date(dateTime);
  
  if (isNaN(d.getTime())) return '';
  
  const date = formatDate(d);
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');
  
  return `${date} ${hours}:${minutes}:${seconds}`;
}