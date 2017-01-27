import copy
import sys

PLUS = '+'
MINUS = '-'


class Number:
    def __init__(self):
        self.value = '#'
        self.next = None


class LongNumber(object):
    def __init__(self, value=0):
        self.head = Number()
        self.sign = PLUS
        self._fill(str(value))

    def __str__(self):
        result = ""
        p = self.head.next

        while p is not None:
            result = str(p.value) + result
            p = p.next

        if not self._is_zero() and self.sign != PLUS:
            result = MINUS + result

        return result

    def __neg__(self):
        result = self.copy()
        if self._is_zero():
            return result

        if self.sign == PLUS:
            result.sign = MINUS
        else:
            result.sign = PLUS

        return result

    def __abs__(self):
        result = self.copy()
        result.sign = PLUS
        return result

    def __eq__(self, other):
        p1 = self.head.next
        p2 = other.head.next

        if self.sign == other.sign:
            equal = True
        else:
            equal = False

        while p1 and p2 and equal:
            equal = (p1.value == p2.value)
            p1 = p1.next
            p2 = p2.next

        if not p1 and not p2 and equal:
            return True
        else:
            return False

    def __len__(self):
        count = 0
        p = self.head
        while p.next:
            count += 1
            p = p.next
        return count

    def __lt__(self, other):
        if self.sign == PLUS and other.sign == MINUS:
            return False
        elif self.sign == MINUS and other.sign == PLUS:
            return True
        elif self.sign == MINUS and other.sign == MINUS:
            return other._low_then(self)
        else:
            return self._low_then(other)

    def __le__(self, other):
        return True if self < other or self == other else False

    def __ne__(self, other):
        if self == other:
            return False
        else:
            return True

    def __gt__(self, other):
        return True if other < self else False

    def __ge__(self, other):
        return True if self < other else False

    def __add__(self, other):
        if self.sign == PLUS and other.sign == PLUS:
            return self._simple_add(other)
        elif self.sign == MINUS and other.sign == MINUS:
            result = self._simple_add(other)
            result.sign = MINUS
            return result
        elif self.sign == MINUS and other.sign == PLUS:
            a_self = abs(self)
            a_other = abs(other)

            if a_other > a_self:
                result = a_other._simple_sub(a_self)
                result.sign = PLUS
            else:
                result = a_self._simple_sub(a_other)
                result.sign = MINUS
            return result

        else:
            return other + self

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if (self.sign == PLUS and other.sign == PLUS) or (self.sign == MINUS and other.sign == MINUS):
            return self._simple_mul(other)
        elif self.sign == MINUS and other.sign == PLUS:
            return -(self._simple_mul(other))
        else:
            return other * self

    def __div__(self, other):
        if other._is_zero():
            raise ZeroDivisionError()
        elif self.sign == MINUS and other.sign == MINUS:
            result = self._simple_div(other)
            result.sign = PLUS
        elif self.sign == PLUS and other.sign == MINUS:
            result = self._simple_div(other)
            result.sign = MINUS
        elif self.sign == MINUS and other.sign == PLUS:
            result = self._simple_div(other)
            result.sign = MINUS
        else:
            result = self._simple_div(other)
            result.sign = PLUS

        result._is_zero()
        return result

    def __mod__(self, other):
        if other._is_zero():
            raise ZeroDivisionError()
        else:
            result = self - ((self / other) * other)
        result._is_zero()
        return result

    def _fill(self, str_value):
        str_value = str(str_value)
        self._del()

        if str_value and str_value[0] == MINUS:
            self.sign = MINUS
            str_value = str_value[1:]

        if str_value and str_value[0] == PLUS:
            str_value = str_value[1:]

        for value in str_value:
            x = int(value)
            self._add_value(x)

        if str_value:
            self._reduce_zeros()
            self._is_zero()

    def _del(self):
        self.head.next = None
        self.sign = PLUS

    def _add_value(self, value):
        tmp = Number()
        tmp.value = value
        tmp.next = self.head.next
        self.head.next = tmp

    def _reduce_zeros(self):
        p = self.head.next
        mark = None

        while p.next:
            if p.next.value != 0:
                mark = p
            p = p.next

        if mark:
            mark.next.next = None
        else:
            self.head.next.next = None

    def _is_zero(self):
        if self.head.next and self.head.next.value == 0 and self.head.next.next is None:
            self.sign = PLUS
            return True
        else:
            return False

    def _x10mul(self, count=1):
        for i in xrange(count):
            self._add_value(0)

    def _x10div(self, count=1):
        for i in xrange(count):
            self.head.next = self.head.next.next

    def _low_then(self, other):
        if len(self) < len(other):
            return True
        elif len(self) > len(other):
            return False
        else:
            c_self = self.copy()
            c_other = other.copy()
            c_self.reverse()
            c_other.reverse()
            p1 = c_self.head.next
            p2 = c_other.head.next

            while p1.value == p2.value and p1.next:
                p1 = p1.next
                p2 = p2.next

            if p1.value < p2.value:
                return True
            else:
                return False

    def _sub_left(self, other):
        a_other = abs(other)
        a_other._x10mul(len(self) - len(other))

        if a_other <= self:
            return self - a_other
        else:
            a_other._x10div(1)
            return self - a_other

    def _simple_add(self, other):
        result = LongNumber()
        carrier = 0
        p1 = self.head.next
        p2 = other.head.next
        p3 = result.head

        while not (p1 is None and p2 is None):
            if p1 is not None and p2 is None:
                p3.next = Number()
                p3 = p3.next
                p3.value = (p1.value + carrier) % 10
                carrier = (p1.value + carrier) / 10
                p1 = p1.next

            if p1 is None and p2 is not None:
                p3.next = Number()
                p3 = p3.next
                p3.value = (p2.value + carrier) % 10
                carrier = (p2.value + carrier) / 10
                p2 = p2.next

            if p1 is not None and p2 is not None:
                p3.next = Number()
                p3 = p3.next
                p3.value = (p2.value + carrier + p1.value) % 10
                carrier = (p2.value + carrier + p1.value) / 10
                p1 = p1.next
                p2 = p2.next

        if carrier != 0:
            p3.next = Number()
            p3 = p3.next
            p3.value = carrier

        return result

    def _simple_sub(self, other):
        result = LongNumber()
        carrier = 0
        p1 = self.head.next
        p2 = other.head.next
        p3 = result.head

        while p1 is not None:
            if p1 is not None and p2 is None:
                p3.next = Number()
                p3 = p3.next
                p3.value = (p1.value - carrier)

                if p3.value < 0:
                    p3.value += 10
                    carrier = 1
                else:
                    carrier = 0

                p1 = p1.next

            if p1 is not None and p2 is not None:
                p3.next = Number()
                p3 = p3.next
                p3.value = (p1.value - p2.value - carrier)

                if p3.value < 0:
                    p3.value += 10
                    carrier = 1
                else:
                    carrier = 0

                p2 = p2.next
                p1 = p1.next

        result._reduce_zeros()
        return result

    def _simple_mul(self, other):
        summa = LongNumber()
        tmp = LongNumber()
        p2 = other.head.next
        level = 0

        while p2:
            carrier = 0
            tresult = tmp.head
            p1 = self.head.next

            while p1:
                tresult.next = Number()
                tresult = tresult.next
                tresult.value = ((p1.value * p2.value) + carrier) % 10
                carrier = ((p1.value * p2.value) + carrier) / 10
                p1 = p1.next

            tresult.next = Number()
            tresult = tresult.next
            tresult.value = carrier
            tmp._x10mul(level)
            summa = summa + tmp
            tmp = LongNumber()
            level += 1
            p2 = p2.next

        summa._reduce_zeros()
        return summa

    def _simple_div(self, other):
        a_self = abs(self)
        a_other = abs(other)
        result = LongNumber()
        delit = a_other.copy()
        count = 0

        while a_other < a_self:
            count += 1
            a_other._x10mul()
        a_other._x10div()
        count -= 1
        w1 = len(self)
        w2 = len(other)
        e1 = int(str(self))
        e2 = int(str(other))

        if w1 > 10 and w2 > 10:
            result._fill(str(e1 / e2))
            return result

        j = 0

        while j <= count:
            C = LongNumber()
            i = 0
            C._fill(i)

            while C * a_other <= a_self:
                i += 1
                C._fill(i)
            i -= 1

            if i == -1:
                i = 0

            result._add_value(i)
            C._fill(i)
            a_self = a_self - (C * a_other)

            if a_other != delit:
                a_other._x10div()
            j += 1

        result._reduce_zeros()
        return result

    def copy(self):
        return copy.deepcopy(self)

    def empty(self):
        return not self.head.next

    def reverse(self):
        t1 = self.head.next
        s = None
        while t1 is not None:
            p = t1
            t1 = t1.next
            p.next = s
            s = p
        self.head.next = s

if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    a = LongNumber('99984837748376451364819236574859939485762364524398124012957436566329491329590543697873549698543600212341324245234654226076788461115424524353246354635463546435333122344')
    b = LongNumber('994352384587234761191230401275643756743825893458010951351135515155131486122134648687953213563546354634563456354624123423452345354643221125')
    c = LongNumber('1234125643529966029034852967825687348576982745972093374225875529724523452435324523467465476567543635463456435')
    x = a * b + c
    print 'A -> ', a
    print 'B -> ', b
    print 'C -> ', c
    print 'X -> ', x
    print 'X div B -> ', x / b
    print 'X mod B -> ', x % b
