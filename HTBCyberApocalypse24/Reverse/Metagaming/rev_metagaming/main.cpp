// Use MSVC or `g++ -std=c++20`

#include <cstdint>
#include <array>
#include <iostream>
#include <numeric>
#include <type_traits>
#include <algorithm>
#include <variant>

#ifndef __noop
#define __noop
#endif

constexpr uint32_t rotr(const uint32_t value, const int shift) {
    return std::rotr(value, shift);
}

constexpr uint32_t rotl(const uint32_t value, const int shift) {
    return std::rotl(value, shift);
}

template<class, class>
constexpr bool is_same_v = false;

template<class Ty>
constexpr bool is_same_v<Ty, Ty> = true;

struct true_t {};
struct false_t {};

template<class Ty>
concept bool_t = is_same_v<Ty, true_t> || is_same_v<Ty, false_t>;

template<bool Val>
struct to_bool {
    using T = false_t;
};
template<>
struct to_bool<true> {
    using T = true_t;
};
template<bool Val>
using to_bool_t = typename to_bool<Val>::T;
template<bool_t Ty>
constexpr bool from_bool_v = is_same_v<Ty, true_t>;

template<char C>
struct char_value_t {
    [[nodiscard]] constexpr static char value() {
        return C;
    }
};

struct a : char_value_t<'a'> {};
struct b : char_value_t<'b'> {};
struct c : char_value_t<'c'> {};
struct d : char_value_t<'d'> {};
struct e : char_value_t<'e'> {};
struct f : char_value_t<'f'> {};
struct g : char_value_t<'g'> {};
struct h : char_value_t<'h'> {};
struct i : char_value_t<'i'> {};
struct j : char_value_t<'j'> {};
struct k : char_value_t<'k'> {};
struct l : char_value_t<'l'> {};
struct m : char_value_t<'m'> {};
struct n : char_value_t<'n'> {};
struct o : char_value_t<'o'> {};
struct p : char_value_t<'p'> {};
struct q : char_value_t<'q'> {};
struct r : char_value_t<'r'> {};
struct s : char_value_t<'s'> {};
struct t : char_value_t<'t'> {};
struct u : char_value_t<'u'> {};
struct v : char_value_t<'v'> {};
struct w : char_value_t<'w'> {};
struct x : char_value_t<'x'> {};
struct y : char_value_t<'y'> {};
struct z : char_value_t<'z'> {};
struct A : char_value_t<'A'> {};
struct B : char_value_t<'B'> {};
struct C : char_value_t<'C'> {};
struct D : char_value_t<'D'> {};
struct E : char_value_t<'E'> {};
struct F : char_value_t<'F'> {};
struct G : char_value_t<'G'> {};
struct H : char_value_t<'H'> {};
struct I : char_value_t<'I'> {};
struct J : char_value_t<'J'> {};
struct K : char_value_t<'K'> {};
struct L : char_value_t<'L'> {};
struct M : char_value_t<'M'> {};
struct N : char_value_t<'N'> {};
struct O : char_value_t<'O'> {};
struct P : char_value_t<'P'> {};
struct Q : char_value_t<'Q'> {};
struct R : char_value_t<'R'> {};
struct S : char_value_t<'S'> {};
struct T : char_value_t<'T'> {};
struct U : char_value_t<'U'> {};
struct V : char_value_t<'V'> {};
struct W : char_value_t<'W'> {};
struct X : char_value_t<'X'> {};
struct Y : char_value_t<'Y'> {};
struct Z : char_value_t<'Z'> {};
struct num_1 : char_value_t<'1'> {};
struct num_2 : char_value_t<'2'> {};
struct num_3 : char_value_t<'3'> {};
struct num_4 : char_value_t<'4'> {};
struct num_5 : char_value_t<'5'> {};
struct num_6 : char_value_t<'6'> {};
struct num_7 : char_value_t<'7'> {};
struct num_8 : char_value_t<'8'> {};
struct num_9 : char_value_t<'9'> {};
struct num_0 : char_value_t<'0'> {};
// SOMEWHAT SPECIAL CHARACTERS
struct bracket_open : char_value_t<'{'> {};
struct bracket_close : char_value_t<'}'> {};
struct underscore : char_value_t<'_'> {};

template<class Ty, class... Types>
concept is_any_of_t = std::disjunction_v<std::is_same<Ty, Types>...>;

template<typename Ty>
concept any_legit_char_t = is_any_of_t<Ty, a, b, c, d, e, f, g, h, i, j, k, l, m, n,
                                       o, p, q, r, s, t, u, v, w, x, y, z, A, B, C, D,
                                       E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T,
                                       U, V, W, X, Y, Z, num_1, num_2, num_3, num_4, num_5,
                                       num_6, num_7, num_8, num_9, num_0, bracket_open,
                                       bracket_close, underscore>;

template<class... values>
struct flag_t {
    [[nodiscard]] static constexpr size_t size() {
        return sizeof...(values);
    }

    template<typename Ty = char>
    [[nodiscard]] static constexpr Ty at(const std::size_t i) {
        constexpr char values_values[] = {values::value()...};
        return static_cast<Ty>(values_values[i]);
    }
};

template<size_t Footprint>
struct cxstring {
    char data[Footprint]{};
    [[nodiscard]] constexpr size_t size() const {
        return Footprint - 1;
    }
    constexpr /* implicit */ cxstring(const char (&init)[Footprint]) {// NOLINT
        std::copy_n(init, Footprint, data);
    }
};

template<auto str>
struct type_string {
    [[nodiscard]] static constexpr const char *data() {
        return str.data;
    }
    [[nodiscard]] static constexpr size_t size() {
        return str.size();
    }
};

template<class P>
auto parse_flag(P) -> P { return {}; }

template<char Chr, char... Rest, class... Bs>
auto parse_flag(flag_t<Bs...>) -> decltype(parse_flag<Rest...>(flag_t<Bs..., char_value_t<Chr>>{})) { return {}; }

template<class lambda_t, size_t... I>
constexpr auto make_flag(lambda_t lambda [[maybe_unused]], std::index_sequence<I...>) {
    return decltype(parse_flag<lambda()[I]...>(flag_t<>{})){};
}

template<cxstring str>
constexpr auto operator"" _flag() noexcept {
    constexpr auto s = type_string<str>{};
    return make_flag([&]() constexpr { return (s.data()); }, std::make_index_sequence<s.size()>{});
}

struct insn_t {
    uint32_t opcode = 0;
    uint32_t op0 = 0;
    uint32_t op1 = 0;
};

template<typename = std::monostate>
concept always_false_v = false;

template<insn_t>
concept always_false_insn_v = false;

template<flag_t Flag, insn_t... Instructions>
struct program_t {
    using R = std::array<uint32_t, 15>;

    template<insn_t Insn>
    static constexpr void execute_one(R &regs) {
        if constexpr (Insn.opcode == 0) {
            regs[Insn.op0] = Flag.at(Insn.op1);
        } else if constexpr (Insn.opcode == 1) {
            regs[Insn.op0] = Insn.op1;
        } else if constexpr (Insn.opcode == 2) {
            regs[Insn.op0] ^= Insn.op1;
        } else if constexpr (Insn.opcode == 3) {
            regs[Insn.op0] ^= regs[Insn.op1];
        } else if constexpr (Insn.opcode == 4) {
            regs[Insn.op0] |= Insn.op1;
        } else if constexpr (Insn.opcode == 5) {
            regs[Insn.op0] |= regs[Insn.op1];
        } else if constexpr (Insn.opcode == 6) {
            regs[Insn.op0] &= Insn.op1;
        } else if constexpr (Insn.opcode == 7) {
            regs[Insn.op0] &= regs[Insn.op1];
        } else if constexpr (Insn.opcode == 8) {
            regs[Insn.op0] += Insn.op1;
        } else if constexpr (Insn.opcode == 9) {
            regs[Insn.op0] += regs[Insn.op1];
        } else if constexpr (Insn.opcode == 10) {
            regs[Insn.op0] -= Insn.op1;
        } else if constexpr (Insn.opcode == 11) {
            regs[Insn.op0] -= regs[Insn.op1];
        } else if constexpr (Insn.opcode == 12) {
            regs[Insn.op0] *= Insn.op1;
        } else if constexpr (Insn.opcode == 13) {
            regs[Insn.op0] *= regs[Insn.op1];
        } else if constexpr (Insn.opcode == 14) {
            __noop;
        } else if constexpr (Insn.opcode == 15) {
            __noop;
            __noop;
        } else if constexpr (Insn.opcode == 16) {
            regs[Insn.op0] = rotr(regs[Insn.op0], Insn.op1);
        } else if constexpr (Insn.opcode == 17) {
            regs[Insn.op0] = rotr(regs[Insn.op0], regs[Insn.op1]);
        } else if constexpr (Insn.opcode == 18) {
            regs[Insn.op0] = rotl(regs[Insn.op0], Insn.op1);
        } else if constexpr (Insn.opcode == 19) {
            regs[Insn.op0] = rotl(regs[Insn.op0], regs[Insn.op1]);
        } else if constexpr (Insn.opcode == 20) {
            regs[Insn.op0] = regs[Insn.op1];
        } else if constexpr (Insn.opcode == 21) {
            regs[Insn.op0] = 0;
        } else if constexpr (Insn.opcode == 22) {
            regs[Insn.op0] >>= Insn.op1;
        } else if constexpr (Insn.opcode == 23) {
            regs[Insn.op0] >>= regs[Insn.op1];
        } else if constexpr (Insn.opcode == 24) {
            regs[Insn.op0] <<= Insn.op1;
        } else if constexpr (Insn.opcode == 25) {
            regs[Insn.op0] <<= regs[Insn.op1];
        } else {
            static_assert(always_false_insn_v<Insn>);
        }
    }

    template<std::size_t... Is>
    static constexpr void execute_impl(R &regs, std::index_sequence<Is...>) {
        (execute_one<Instructions>(regs), ...);
    }

    static constexpr void execute(R &regs) {
        execute_impl(regs, std::make_index_sequence<sizeof...(Instructions)>{});
    }

    static constexpr R registers = []() -> R {
        R arr = {};
        execute(arr);
        return arr;
    }();
};

int main() {
    /// Modify this text              vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    [[maybe_unused]] auto flag = "HTB{___________________________________}"_flag;
    /// Modify this text              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    static_assert(decltype(flag)::size() == 40);

    using program = program_t<flag, insn_t(12, 13, 10), insn_t(21, 0, 0), insn_t(0, 13, 13), insn_t(0, 14, 0), insn_t(15, 11, 12), insn_t(24, 14, 0), insn_t(5, 0, 14), insn_t(0, 14, 1), insn_t(7, 11, 11), insn_t(24, 14, 8), insn_t(5, 0, 14), insn_t(0, 14, 2), insn_t(2, 10, 11), insn_t(24, 14, 16), insn_t(18, 12, 11), insn_t(5, 0, 14), insn_t(0, 14, 3), insn_t(0, 11, 11), insn_t(24, 14, 24), insn_t(13, 10, 10), insn_t(5, 0, 14), insn_t(2, 11, 13), insn_t(21, 1, 0), insn_t(0, 14, 4), insn_t(24, 14, 0), insn_t(5, 1, 14), insn_t(6, 11, 12), insn_t(0, 14, 5), insn_t(8, 10, 10), insn_t(24, 14, 8), insn_t(11, 12, 11), insn_t(5, 1, 14), insn_t(0, 14, 6), insn_t(0, 12, 10), insn_t(24, 14, 16), insn_t(9, 10, 13), insn_t(5, 1, 14), insn_t(0, 14, 7), insn_t(13, 12, 12), insn_t(24, 14, 24), insn_t(15, 10, 12), insn_t(5, 1, 14), insn_t(21, 2, 0), insn_t(20, 13, 13), insn_t(0, 14, 8), insn_t(24, 14, 0), insn_t(19, 10, 11), insn_t(5, 2, 14), insn_t(6, 12, 10), insn_t(0, 14, 9), insn_t(8, 11, 11), insn_t(24, 14, 8), insn_t(5, 2, 14), insn_t(0, 14, 10), insn_t(4, 11, 12), insn_t(24, 14, 16), insn_t(5, 2, 14), insn_t(0, 14, 11), insn_t(24, 14, 24), insn_t(4, 13, 12), insn_t(5, 2, 14), insn_t(21, 3, 0), insn_t(14, 10, 12), insn_t(0, 14, 12), insn_t(13, 10, 11), insn_t(24, 14, 0), insn_t(16, 10, 10), insn_t(5, 3, 14), insn_t(5, 11, 12), insn_t(0, 14, 13), insn_t(12, 10, 13), insn_t(24, 14, 8), insn_t(2, 10, 13), insn_t(5, 3, 14), insn_t(20, 11, 11), insn_t(0, 14, 14), insn_t(24, 14, 16), insn_t(18, 13, 11), insn_t(5, 3, 14), insn_t(6, 11, 13), insn_t(0, 14, 15), insn_t(24, 14, 24), insn_t(4, 11, 10), insn_t(5, 3, 14), insn_t(21, 4, 0), insn_t(15, 13, 11), insn_t(0, 14, 16), insn_t(6, 10, 10), insn_t(24, 14, 0), insn_t(14, 10, 12), insn_t(5, 4, 14), insn_t(0, 14, 17), insn_t(12, 13, 13), insn_t(24, 14, 8), insn_t(19, 11, 10), insn_t(5, 4, 14), insn_t(0, 14, 18), insn_t(17, 13, 12), insn_t(24, 14, 16), insn_t(5, 4, 14), insn_t(0, 14, 19), insn_t(24, 14, 24), insn_t(21, 12, 10), insn_t(5, 4, 14), insn_t(13, 13, 10), insn_t(21, 5, 0), insn_t(0, 14, 20), insn_t(19, 10, 13), insn_t(24, 14, 0), insn_t(5, 5, 14), insn_t(0, 14, 21), insn_t(24, 14, 8), insn_t(8, 13, 13), insn_t(5, 5, 14), insn_t(0, 14, 22), insn_t(16, 13, 11), insn_t(24, 14, 16), insn_t(10, 10, 13), insn_t(5, 5, 14), insn_t(7, 10, 12), insn_t(0, 14, 23), insn_t(19, 13, 10), insn_t(24, 14, 24), insn_t(5, 5, 14), insn_t(17, 12, 10), insn_t(21, 6, 0), insn_t(16, 11, 10), insn_t(0, 14, 24), insn_t(24, 14, 0), insn_t(10, 11, 10), insn_t(5, 6, 14), insn_t(0, 14, 25), insn_t(24, 14, 8), insn_t(7, 10, 12), insn_t(5, 6, 14), insn_t(0, 14, 26), insn_t(16, 12, 11), insn_t(24, 14, 16), insn_t(3, 11, 10), insn_t(5, 6, 14), insn_t(15, 11, 13), insn_t(0, 14, 27), insn_t(4, 12, 13), insn_t(24, 14, 24), insn_t(5, 6, 14), insn_t(14, 11, 13), insn_t(21, 7, 0), insn_t(0, 14, 28), insn_t(21, 13, 11), insn_t(24, 14, 0), insn_t(7, 12, 11), insn_t(5, 7, 14), insn_t(17, 11, 10), insn_t(0, 14, 29), insn_t(24, 14, 8), insn_t(5, 7, 14), insn_t(0, 14, 30), insn_t(12, 10, 10), insn_t(24, 14, 16), insn_t(5, 7, 14), insn_t(0, 14, 31), insn_t(20, 10, 10), insn_t(24, 14, 24), insn_t(5, 7, 14), insn_t(21, 8, 0), insn_t(18, 10, 12), insn_t(0, 14, 32), insn_t(9, 11, 11), insn_t(24, 14, 0), insn_t(21, 12, 11), insn_t(5, 8, 14), insn_t(0, 14, 33), insn_t(24, 14, 8), insn_t(19, 10, 13), insn_t(5, 8, 14), insn_t(8, 12, 13), insn_t(0, 14, 34), insn_t(24, 14, 16), insn_t(5, 8, 14), insn_t(8, 10, 10), insn_t(0, 14, 35), insn_t(24, 14, 24), insn_t(21, 13, 10), insn_t(5, 8, 14), insn_t(0, 12, 10), insn_t(21, 9, 0), insn_t(0, 14, 36), insn_t(24, 14, 0), insn_t(5, 9, 14), insn_t(17, 11, 11), insn_t(0, 14, 37), insn_t(14, 10, 13), insn_t(24, 14, 8), insn_t(5, 9, 14), insn_t(4, 10, 11), insn_t(0, 14, 38), insn_t(13, 11, 13), insn_t(24, 14, 16), insn_t(5, 9, 14), insn_t(0, 14, 39), insn_t(10, 11, 10), insn_t(24, 14, 24), insn_t(20, 13, 13), insn_t(5, 9, 14), insn_t(6, 12, 11), insn_t(21, 14, 0), insn_t(8, 0, 2769503260), insn_t(10, 0, 997841014), insn_t(19, 12, 11), insn_t(2, 0, 4065997671), insn_t(5, 13, 11), insn_t(8, 0, 690011675), insn_t(15, 11, 11), insn_t(8, 0, 540576667), insn_t(2, 0, 1618285201), insn_t(8, 0, 1123989331), insn_t(8, 0, 1914950564), insn_t(8, 0, 4213669998), insn_t(21, 13, 11), insn_t(8, 0, 1529621790), insn_t(10, 0, 865446746), insn_t(2, 10, 11), insn_t(8, 0, 449019059), insn_t(16, 13, 11), insn_t(8, 0, 906976959), insn_t(6, 10, 10), insn_t(8, 0, 892028723), insn_t(10, 0, 1040131328), insn_t(2, 0, 3854135066), insn_t(2, 0, 4133925041), insn_t(2, 0, 1738396966), insn_t(2, 12, 12), insn_t(8, 0, 550277338), insn_t(10, 0, 1043160697), insn_t(2, 1, 1176768057), insn_t(10, 1, 2368952475), insn_t(8, 12, 11), insn_t(2, 1, 2826144967), insn_t(8, 1, 1275301297), insn_t(10, 1, 2955899422), insn_t(2, 1, 2241699318), insn_t(12, 11, 10), insn_t(8, 1, 537794314), insn_t(11, 13, 10), insn_t(8, 1, 473021534), insn_t(17, 12, 13), insn_t(8, 1, 2381227371), insn_t(10, 1, 3973380876), insn_t(10, 1, 1728990628), insn_t(6, 11, 13), insn_t(8, 1, 2974252696), insn_t(0, 11, 11), insn_t(8, 1, 1912236055), insn_t(2, 1, 3620744853), insn_t(3, 10, 13), insn_t(2, 1, 2628426447), insn_t(11, 13, 12), insn_t(10, 1, 486914414), insn_t(16, 11, 12), insn_t(10, 1, 1187047173), insn_t(14, 12, 11), insn_t(2, 2, 3103274804), insn_t(13, 10, 10), insn_t(8, 2, 3320200805), insn_t(8, 2, 3846589389), insn_t(1, 13, 13), insn_t(2, 2, 2724573159), insn_t(10, 2, 1483327425), insn_t(2, 2, 1957985324), insn_t(14, 13, 12), insn_t(10, 2, 1467602691), insn_t(8, 2, 3142557962), insn_t(2, 13, 12), insn_t(2, 2, 2525769395), insn_t(8, 2, 3681119483), insn_t(8, 12, 11), insn_t(10, 2, 1041439413), insn_t(10, 2, 1042206298), insn_t(2, 2, 527001246), insn_t(20, 10, 13), insn_t(10, 2, 855860613), insn_t(8, 10, 10), insn_t(8, 2, 1865979270), insn_t(1, 13, 10), insn_t(8, 2, 2752636085), insn_t(2, 2, 1389650363), insn_t(10, 2, 2721642985), insn_t(18, 10, 11), insn_t(8, 2, 3276518041), insn_t(15, 10, 10), insn_t(2, 2, 1965130376), insn_t(2, 3, 3557111558), insn_t(2, 3, 3031574352), insn_t(16, 12, 10), insn_t(10, 3, 4226755821), insn_t(8, 3, 2624879637), insn_t(8, 3, 1381275708), insn_t(2, 3, 3310620882), insn_t(2, 3, 2475591380), insn_t(8, 3, 405408383), insn_t(2, 3, 2291319543), insn_t(0, 12, 12), insn_t(8, 3, 4144538489), insn_t(2, 3, 3878256896), insn_t(6, 11, 10), insn_t(10, 3, 2243529248), insn_t(10, 3, 561931268), insn_t(11, 11, 12), insn_t(10, 3, 3076955709), insn_t(18, 12, 13), insn_t(8, 3, 2019584073), insn_t(10, 13, 12), insn_t(8, 3, 1712479912), insn_t(18, 11, 11), insn_t(2, 3, 2804447380), insn_t(17, 10, 10), insn_t(10, 3, 2957126100), insn_t(18, 13, 13), insn_t(8, 3, 1368187437), insn_t(17, 10, 12), insn_t(8, 3, 3586129298), insn_t(10, 4, 1229526732), insn_t(19, 11, 11), insn_t(10, 4, 2759768797), insn_t(1, 10, 13), insn_t(2, 4, 2112449396), insn_t(10, 4, 1212917601), insn_t(2, 4, 1524771736), insn_t(8, 4, 3146530277), insn_t(2, 4, 2997906889), insn_t(16, 12, 10), insn_t(8, 4, 4135691751), insn_t(8, 4, 1960868242), insn_t(6, 12, 12), insn_t(10, 4, 2775657353), insn_t(16, 10, 13), insn_t(8, 4, 1451259226), insn_t(8, 4, 607382171), insn_t(13, 13, 13), insn_t(10, 4, 357643050), insn_t(2, 4, 2020402776), insn_t(8, 5, 2408165152), insn_t(13, 12, 10), insn_t(2, 5, 806913563), insn_t(10, 5, 772591592), insn_t(20, 13, 11), insn_t(2, 5, 2211018781), insn_t(10, 5, 2523354879), insn_t(8, 5, 2549720391), insn_t(2, 5, 3908178996), insn_t(2, 5, 1299171929), insn_t(8, 5, 512513885), insn_t(10, 5, 2617924552), insn_t(1, 12, 13), insn_t(8, 5, 390960442), insn_t(12, 11, 13), insn_t(8, 5, 1248271133), insn_t(8, 5, 2114382155), insn_t(1, 10, 13), insn_t(10, 5, 2078863299), insn_t(20, 12, 12), insn_t(8, 5, 2857504053), insn_t(10, 5, 4271947727), insn_t(2, 6, 2238126367), insn_t(2, 6, 1544827193), insn_t(8, 6, 4094800187), insn_t(2, 6, 3461906189), insn_t(10, 6, 1812592759), insn_t(2, 6, 1506702473), insn_t(8, 6, 536175198), insn_t(2, 6, 1303821297), insn_t(8, 6, 715409343), insn_t(2, 6, 4094566992), insn_t(14, 10, 11), insn_t(2, 6, 1890141105), insn_t(0, 13, 13), insn_t(2, 6, 3143319360), insn_t(10, 7, 696930856), insn_t(2, 7, 926450200), insn_t(8, 7, 352056373), insn_t(20, 13, 11), insn_t(10, 7, 3857703071), insn_t(8, 7, 3212660135), insn_t(5, 12, 10), insn_t(10, 7, 3854876250), insn_t(21, 12, 11), insn_t(8, 7, 3648688720), insn_t(2, 7, 2732629817), insn_t(4, 10, 12), insn_t(10, 7, 2285138643), insn_t(18, 10, 13), insn_t(2, 7, 2255852466), insn_t(2, 7, 2537336944), insn_t(3, 10, 13), insn_t(2, 7, 4257606405), insn_t(10, 8, 3703184638), insn_t(7, 11, 10), insn_t(10, 8, 2165056562), insn_t(8, 8, 2217220568), insn_t(19, 10, 12), insn_t(8, 8, 2088084496), insn_t(15, 13, 10), insn_t(8, 8, 443074220), insn_t(16, 13, 12), insn_t(10, 8, 1298336973), insn_t(2, 13, 11), insn_t(8, 8, 822378456), insn_t(19, 11, 12), insn_t(8, 8, 2154711985), insn_t(0, 11, 12), insn_t(10, 8, 430757325), insn_t(2, 12, 10), insn_t(2, 8, 2521672196), insn_t(10, 9, 532704100), insn_t(10, 9, 2519542932), insn_t(2, 9, 2451309277), insn_t(2, 9, 3957445476), insn_t(5, 10, 10), insn_t(8, 9, 2583554449), insn_t(10, 9, 1149665327), insn_t(12, 13, 12), insn_t(8, 9, 3053959226), insn_t(0, 10, 10), insn_t(8, 9, 3693780276), insn_t(15, 11, 10), insn_t(2, 9, 609918789), insn_t(2, 9, 2778221635), insn_t(16, 13, 10), insn_t(8, 9, 3133754553), insn_t(8, 11, 13), insn_t(8, 9, 3961507338), insn_t(2, 9, 1829237263), insn_t(16, 11, 13), insn_t(2, 9, 2472519933), insn_t(6, 12, 12), insn_t(8, 9, 4061630846), insn_t(10, 9, 1181684786), insn_t(13, 10, 11), insn_t(10, 9, 390349075), insn_t(8, 9, 2883917626), insn_t(10, 9, 3733394420), insn_t(10, 12, 12), insn_t(2, 9, 3895283827), insn_t(20, 10, 11), insn_t(2, 9, 2257053750), insn_t(10, 9, 2770821931), insn_t(18, 10, 13), insn_t(2, 9, 477834410), insn_t(19, 13, 12), insn_t(3, 0, 1), insn_t(12, 12, 12), insn_t(3, 1, 2), insn_t(11, 13, 11), insn_t(3, 2, 3), insn_t(3, 3, 4), insn_t(3, 4, 5), insn_t(1, 13, 13), insn_t(3, 5, 6), insn_t(7, 11, 11), insn_t(3, 6, 7), insn_t(4, 10, 12), insn_t(3, 7, 8), insn_t(18, 12, 12), insn_t(3, 8, 9), insn_t(21, 12, 10), insn_t(3, 9, 10)>;
    static_assert(program::registers[0] == 0x3ee88722 && program::registers[1] == 0xecbdbe2 && program::registers[2] == 0x60b843c4 && program::registers[3] == 0x5da67c7 && program::registers[4] == 0x171ef1e9 && program::registers[5] == 0x52d5b3f7 && program::registers[6] == 0x3ae718c0 && program::registers[7] == 0x8b4aacc2 && program::registers[8] == 0xe5cf78dd && program::registers[9] == 0x4a848edf && program::registers[10] == 0x8f && program::registers[11] == 0x4180000 && program::registers[12] == 0x0 && program::registers[13] == 0xd && program::registers[14] == 0x0, "Ah! Your flag is invalid.");
}
