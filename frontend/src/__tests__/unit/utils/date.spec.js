/**
 * 日期工具测试
 */
import { describe, it, expect } from 'vitest'

describe('Date Utilities', () => {
  it('should format date correctly', () => {
    const date = new Date('2026-01-28')
    const formatted = date.toLocaleDateString('zh-CN')
    expect(formatted).toBeDefined()
    expect(formatted).toContain('2026')
  })

  it('should calculate days between dates', () => {
    const date1 = new Date('2026-01-01')
    const date2 = new Date('2026-01-08')
    const diffTime = Math.abs(date2 - date1)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    expect(diffDays).toBe(7)
  })

  it('should check if date is today', () => {
    const today = new Date()
    const todayString = today.toDateString()
    const checkDate = new Date(todayString)
    expect(checkDate.toDateString()).toBe(todayString)
  })

  it('should get start of day', () => {
    const date = new Date('2026-01-28T10:30:00')
    const startOfDay = new Date(date.getFullYear(), date.getMonth(), date.getDate())
    expect(startOfDay.getHours()).toBe(0)
    expect(startOfDay.getMinutes()).toBe(0)
    expect(startOfDay.getSeconds()).toBe(0)
  })

  it('should get end of day', () => {
    const date = new Date('2026-01-28T10:30:00')
    const endOfDay = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 23, 59, 59, 999)
    expect(endOfDay.getHours()).toBe(23)
    expect(endOfDay.getMinutes()).toBe(59)
  })

  it('should format time as HH:MM:SS', () => {
    const date = new Date('2026-01-28T14:30:45')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')
    const formatted = `${hours}:${minutes}:${seconds}`
    expect(formatted).toBe('14:30:45')
  })

  it('should add days to date', () => {
    const date = new Date('2026-01-28')
    const newDate = new Date(date)
    newDate.setDate(newDate.getDate() + 7)
    expect(newDate.getDate()).toBe(4)
    expect(newDate.getMonth()).toBe(1) // 二月
  })

  it('should subtract days from date', () => {
    const date = new Date('2026-02-04')
    const newDate = new Date(date)
    newDate.setDate(newDate.getDate() - 7)
    expect(newDate.getDate()).toBe(28)
    expect(newDate.getMonth()).toBe(0) // 一月
  })

  it('should check if date is in the past', () => {
    const pastDate = new Date('2026-01-01')
    const today = new Date()
    expect(pastDate < today).toBe(true)
  })

  it('should check if date is in the future', () => {
    const futureDate = new Date('2027-01-01')
    const today = new Date()
    expect(futureDate > today).toBe(true)
  })

  it('should get week number', () => {
    const date = new Date('2026-01-05') // 第一周
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1)
    const pastDaysOfYear = (date - firstDayOfYear) / 86400000
    const weekNumber = Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7)
    expect(weekNumber).toBe(2)
  })

  it('should get month name', () => {
    const date = new Date('2026-01-28')
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December']
    const monthName = monthNames[date.getMonth()]
    expect(monthName).toBe('January')
  })

  it('should get day name', () => {
    const date = new Date('2026-01-28') // Wednesday
    const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    const dayName = dayNames[date.getDay()]
    expect(dayName).toBe('Wednesday')
  })
})
