describe('Smoke Test', () => {
  it('can view the home page', () => {
    cy.visit('http://localhost:3000');
    cy.contains('Welcome to Leitner Box');
  });
});
