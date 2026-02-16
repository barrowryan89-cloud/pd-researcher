#!/usr/bin/env python3
"""
calc_free.py - Command-Line Calculator
Advanced calculator with math functions, variables, and expression evaluation.
Zero dependencies. Pure Python 3.
"""

import sys
import math
import operator

# Available constants
CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'tau': math.tau,
}

# Available functions
FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,
    'sqrt': math.sqrt,
    'log': math.log10,
    'ln': math.log,
    'log2': math.log2,
    'exp': math.exp,
    'abs': abs,
    'floor': math.floor,
    'ceil': math.ceil,
    'round': round,
    'deg': math.degrees,
    'rad': math.radians,
    'fact': math.factorial,
    'pow': pow,
    'max': max,
    'min': min,
    'sum': sum,
}

class Calculator:
    """Simple expression evaluator."""
    
    def __init__(self):
        self.variables = {}
        self.last_result = None
    
    def evaluate(self, expression: str):
        """Safely evaluate a mathematical expression."""
        # Clean the expression
        expr = expression.strip()
        
        # Handle special commands
        if expr == 'vars':
            return self._show_vars()
        if expr == 'clear':
            self.variables.clear()
            return "Variables cleared"
        if expr == 'help':
            return self._show_help()
        
        # Handle variable assignment
        if '=' in expr and not any(op in expr for op in ['==', '!=', '<=', '>=']):
            parts = expr.split('=', 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                if var_name.isidentifier() and not var_name in FUNCTIONS:
                    try:
                        value = self._eval_expr(parts[1])
                        self.variables[var_name] = value
                        self.last_result = value
                        return f"{var_name} = {value}"
                    except Exception as e:
                        return f"Error: {e}"
        
        # Evaluate expression
        try:
            result = self._eval_expr(expr)
            self.last_result = result
            return result
        except Exception as e:
            return f"Error: {e}"
    
    def _eval_expr(self, expr: str):
        """Evaluate expression with limited safe operations."""
        # Replace constants
        for name, value in CONSTANTS.items():
            expr = expr.replace(name, str(value))
        
        # Replace variables
        for name, value in self.variables.items():
            expr = expr.replace(name, str(value))
        
        # Handle _ (last result)
        if self.last_result is not None:
            expr = expr.replace('_', str(self.last_result))
        
        # Replace ^ with **
        expr = expr.replace('^', '**')
        
        # Create safe namespace
        namespace = {
            '__builtins__': {},
            'math': math,
        }
        namespace.update(FUNCTIONS)
        
        try:
            result = eval(expr, namespace)
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
    
    def _show_vars(self):
        """Show defined variables."""
        if not self.variables:
            return "No variables defined"
        lines = ["Variables:"]
        for name, value in self.variables.items():
            lines.append(f"  {name} = {value}")
        if self.last_result is not None:
            lines.append(f"  _ = {self.last_result} (last result)")
        return "\n".join(lines)
    
    def _show_help(self):
        """Show help text."""
        return """
Calculator Help:

Operators: +, -, *, /, //, %, ** (or ^)
Constants: pi, e, tau
Variables: x = 5, y = x + 3, use _ for last result

Functions:
  Trig: sin, cos, tan, asin, acos, atan
  Hyperbolic: sinh, cosh, tanh
  Math: sqrt, log, ln, log2, exp, abs
        floor, ceil, round, deg, rad, fact
  Other: pow, max, min, sum

Commands:
  vars   - Show defined variables
  clear  - Clear all variables
  help   - Show this help

Examples:
  calc "2 + 3 * 4"
  calc "sin(pi / 2)"
  calc "x = 10"
  calc "x * 2"
  calc "sqrt(16) + pow(2, 3)"
"""

def format_number(num):
    """Format number for display."""
    if isinstance(num, (int, float)):
        if isinstance(num, float):
            # Remove trailing zeros
            s = f"{num:.10f}".rstrip('0').rstrip('.')
            return s
        return str(num)
    return str(num)

def main():
    if len(sys.argv) < 2:
        print("Usage: calc_free.py <expression>")
        print("       calc_free.py interactive")
        print("\nExamples:")
        print('  calc_free.py "2 + 3 * 4"')
        print('  calc_free.py "sin(pi / 2)"')
        print('  calc_free.py "x = 10"')
        print('  calc_free.py interactive')
        print("\nRun 'calc_free.py \"help\"' for detailed help")
        sys.exit(1)
    
    calc = Calculator()
    
    # Check for interactive mode
    if sys.argv[1].lower() == 'interactive':
        print("🧮 Calculator (interactive mode)")
        print("Type 'exit' or 'quit' to exit, 'help' for help")
        print("-" * 40)
        
        while True:
            try:
                expr = input("> ").strip()
                if expr.lower() in ('exit', 'quit'):
                    break
                if not expr:
                    continue
                
                result = calc.evaluate(expr)
                print(format_number(result))
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                break
    else:
        # Single expression mode
        expression = " ".join(sys.argv[1:])
        result = calc.evaluate(expression)
        print(format_number(result))

if __name__ == "__main__":
    main()
