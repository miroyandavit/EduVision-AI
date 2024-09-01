AM_generate_problem_system_inst = """
Given (1) mathematical concepts, and (2) an application area (for example physics, chemistry, etc.),
create an applied math problem solving which must require applying some of the concepts input by the user.

Please follow the instructions below:
* Identify a problem in the specified application area that can be solved using the input concepts . 
* Do not assume any prior knowledge of the application area. 
* Provide all the application-area(physics, economics, etc.) specific term definitions and descriptions if there are any that the user may be unfamilar with.
* Do not provide the solutions or hints on how to solve the problem.
* STRICTLY follow the following example when generating a problem.

**EXAMPLE**

*User*:
Please create an applied math problem in the context of quantum mechanics based on the following concepts:


* first order differential equations
  * finding numerical solutions of differential equations using Euler's method
  * solving variables separable differential equations
  * solving homogeneous differential equations
  * solving linear differential equations including the use of integrating factors
  * Maclaurin series to obtain expansions for e^x, sinx, cosx, ln(1+x), and (1+x)^n 
  * simple substitution, products, integration, and differentiation to obtain other series
  * Maclaurin series developed from differential equations

*Assistant*:

Context: 
In quantum mechanics, the behavior of a particle in a potential field can be described by the Schrödinger equation, which is a differential equation. For simplicity, consider the one-dimensional time-independent Schrödinger equation for a particle of mass ( m ) and energy ( E ) in a potential ( V(x) ):
[ -\frac{\hbar^2}{2m} \frac{d^2 \psi(x)}{dx^2} + V(x)\psi(x) = E\psi(x) ]
where ( \hbar ) (h-bar) is the reduced Planck's constant, ( \psi(x) ) is the wave function of the particle, ( V(x) ) is the potential energy as a function of ( x ), and ( E ) is the total energy of the particle.
To solve this equation, we often need to convert it into a first-order differential equation or use numerical methods.

Problem:

1. Consider a particle of mass ( m ) in a one-dimensional potential well with ( V(x) = 0 ) inside the well (from ( x = 0 ) to ( x = L )) and ( V(x) = \infty ) outside the well. Write down the Schrödinger equation for the particle inside this potential well and solve it to find the wave function ( \psi(x) ) and the corresponding energy levels ( E_n ).

2. Transform the Schrödinger equation into a first-order linear differential equation by expressing ( \psi(x) ) in terms of an exponential function and solve the resulting equation using the method of integrating factors.

3. Use Euler's method to numerically solve the differential equation for the wave function ( \psi(x) ) for a given potential ( V(x) = \frac{1}{2} m \omega^2 x^2 ) (the harmonic oscillator potential) from ( x = -L ) to ( x = L ) with an initial condition ( \psi(0) = 1 ) and ( \psi'(0) = 0 ). Use ( L = 5 ), ( \hbar = 1 ), ( m = 1 ), and ( \omega = 1 ). Choose a step size ( h ) and perform the calculation up to ( x = 5 ).

4. Derive the Maclaurin series expansion for the wave function ( \psi(x) ) of a particle in a potential well and use this series to represent ( \psi(x) ) around ( x = 0 ).

5. Using the Maclaurin series expansions, find the series representation for the wave function of a particle in a harmonic oscillator potential ( V(x) = \frac{1}{2} m \omega^2 x^2 ).

Definitions and Descriptions of Quantum Mechanics Terms:

* Schrödinger Equation: A fundamental equation in quantum mechanics that describes how the quantum state of a physical system changes with space and time.
* Wave Function (( \psi(x) )): A mathematical function representing the quantum state of a particle. The square of the wave function's magnitude, ( |\psi(x)|^2 ), gives the probability density of finding the particle at position ( x ).
* Potential Well: A potential energy function that confines a particle within certain boundaries, outside of which the potential is infinite.
* Harmonic Oscillator: A system in which the force acting on a particle is proportional to its displacement and acts in the direction opposite to the displacement. Its potential energy is quadratic in displacement.
"""

AM_change_problem_system_inst = """
* In your response, provide the full text of the new version of the problem after changing the provided initial problem. Inlucde only the context, problem, the descriptions definitions and nothing else.
"""

AM_generate_sol_system_inst = """
* In your response, include only the solution, nothing else.
"""

AM_change_sol_system_inst = """
* In your response, include only the modified solutions in your response, nothing else.
"""