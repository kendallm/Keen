import os

from keen import Keen

if __name__ == '__main__':
  
  with Keen() as keen:
    to_number = os.environ['TWILIO_TO_NUMBER']
    keen.eye('https://www.ironmaster.com/products/quick-lock-adjustable-dumbbells-75/')
    keen.eye('https://www.ironmaster.com/products/super-bench-pro/')
