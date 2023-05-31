<?php
class Flag {
    public bool $isflag = true;
}

echo urldecode(serialize(new Flag()));