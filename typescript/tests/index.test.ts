import { describe, expect, it } from 'vitest'

describe('Environment Configuration', () => {
  describe('RELACE_API_KEY', () => {
    it('should be defined in import.meta.env', () => {
      expect(import.meta.env.RELACE_API_KEY).toBeDefined()
      expect(typeof import.meta.env.RELACE_API_KEY).toBe('string')
      expect(import.meta.env.RELACE_API_KEY.length).toBeGreaterThan(0)
    })

    it('should match process.env value', () => {
      expect(import.meta.env.RELACE_API_KEY).toEqual(process.env.RELACE_API_KEY)
    })

    it('should not be empty or whitespace only', () => {
      expect(import.meta.env.RELACE_API_KEY.trim()).toBeTruthy()
    })
  })

  describe('Environment variable validation', () => {
    it('should have required environment variables', () => {
      const requiredEnvVars = ['RELACE_API_KEY']

      requiredEnvVars.forEach((envVar) => {
        expect(process.env[envVar], `${envVar} should be defined`).toBeDefined()
        expect(
          process.env[envVar],
          `${envVar} should not be empty`,
        ).toBeTruthy()
      })
    })
  })
})
