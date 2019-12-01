from uno import Buzzer
from time import sleep

bz = Buzzer()
# Play the Do @ 523 Hertz
bz.tone( 523 )
# Wait one second
sleep( 1 )
# Play the Fa @ 349 Hertz
bz.tone( 349 )
# Wait one second
sleep( 1 )
# Silent
bz.tone()
