module.exports = {
  testEnvironment: 'node',
  collectCoverage: true,
  testRegex: '(/__tests__/.*|\\.(test))\\.jsx?$',
  setupFiles: ['dotenv-flow/config'],
  modulePathIgnorePatterns: ['environment/', 'dist/', 'mocks/', 'model/'],
  coveragePathIgnorePatterns: ['node_modules'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node']
};
