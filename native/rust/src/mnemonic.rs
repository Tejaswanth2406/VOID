pub fn major_code(digits: &str) -> String {
    let codes = ["S/Z", "T/D", "N", "M", "R", "L", "J/SH", "K/G", "F/V", "P/B"];
    digits.chars().filter_map(|digit| digit.to_digit(10).map(|index| codes[index as usize])).collect::<Vec<_>>().join(" ")
}

pub fn dominic_code(digits: &str) -> String {
    let codes = ['O', 'A', 'B', 'C', 'D', 'E', 'S', 'G', 'H', 'N'];
    digits.chars().filter_map(|digit| digit.to_digit(10).map(|index| codes[index as usize])).collect()
}

pub fn valid_digits(digits: &str) -> bool { !digits.is_empty() && digits.chars().all(|digit| digit.is_ascii_digit()) }
pub fn major_tokens(digits: &str) -> Vec<String> { major_code(digits).split_whitespace().map(str::to_string).collect() }
pub fn digit_count(digits: &str) -> usize { digits.chars().filter(|digit| digit.is_ascii_digit()).count() }
pub fn normalized_digits(digits: &str) -> String { digits.chars().filter(|digit| digit.is_ascii_digit()).collect() }
pub fn summary(digits: &str) -> String { format!("valid={}, count={}, major={}", valid_digits(digits), digit_count(digits), major_code(digits)) }
