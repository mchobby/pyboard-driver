[This file also exists in ENGLISH](readme_ENG.md)

# Low Frequency PWM - simuler un signal PWM sur un signal très basse fréquence (ou grande période)

--- En cours de traduction ---

When driving devices with high inertia like Iron, Heater, Boiler Plate you are using relay/contactor/SSR (Solid State Relay).

Such interface cannot be driven with Usual PWM signal because it will destroy the relay/SSR due the high switching frequency (500 Hz).

Anything with a frequency higher than 1 Hertz freq is not recommanded in such case.

Because of the High inertia of the controled device, using very low PWM frequency (< 1 Hertz, so a period > 1 sec) doesn't matter and is compatible with Solid State Relay usage.

However, microcontoler PWM routine doesn't accept low frequencies (eg: lower than 7 Hertz for RaspberryPi Pico) so we will have to hack!

# UseCase

For the [plancha-cms project](https://arduino103.blogspot.com/search?q=plancha) (Hot Plate for reflow soldering), we did use an Iron as heater.

![Plancha CMS](docs/_static/usecase.jpg)

Planning a 2 seconds period time as base to control the Iron heater is a raisonnable choice.

This looks appropriate for the following reasons:
* the thermal inertia: the iron metal base takes time to propagate the heat.
* the Solid State Relay: having a switch on/off every 2 seconds is acceptable according the SSR specs.
* We can have a duty cycle from 0 to 100% during that period of 2 seconds... which should offer a great control over the Iron heater)

# How Low Frequency PWM works

The [lfpwm.py](lib/lfpwm.py) library and `LowFreqPWM` do use a timer @ 10 Hertz to generate a low frequency PWM with an extra counter managed in python by the callback routine of the time.

The `LowFreqPWM` class can handle PWM periods of several seconds (<1 Hz) with a duty cycle from 0 to 100% (see `duty_u16()` ).

The period of severals seconds (converted in milliseconds) is used to instead of frequency because it will offer more readable value (than extra small frequency values).

![PWM vs SSR](docs/_static/pwm-vs-ssr.png)

In real world conditions, the transitions are not instantaneous. The SSR (Solid State Relay) do need 8.3ms to switch on (`ton_ms=9` ms) and 10 ms to switch off (`toff_ms=10` ms). We have to keep this in account to avoids excessive switching stress. High inertia devices often consume lot of power, which will stress the the high power swicher (the SSR relay in this case). It is recommended to take it into account.

This bring on two additionnals running conditions:

__Case 1:__ Keeps ON if PWM switching off too close from the end of period
* IF `duty_ms` >= `period_ms - toff_ms` THEN `duty_ms = period_ms` # Keeps ON

__Case 2:__ Keeps OFF if PWM switch on + off too close from the begin of the period
* IF `duty_ms` < `ton_ms + toff_ms` then `duty_ms = 0` # Keeps OFF
