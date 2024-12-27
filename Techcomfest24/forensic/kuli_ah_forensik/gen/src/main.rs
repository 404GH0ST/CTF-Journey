use std::fs::File;
use std::io::{Result, Write};

fn generate_numbers(length: usize) -> Vec<String> {
    let digits = vec!['0', '1', '2'];
    let mut numbers = Vec::new();
    generate_helper(String::new(), length, &digits, &mut numbers);
    numbers
}

fn generate_helper(current: String, length: usize, digits: &[char], numbers: &mut Vec<String>) {
    if length == 0 {
        numbers.push(current);
        return;
    }

    for &digit in digits {
        generate_helper(
            current.clone() + &digit.to_string(),
            length - 1,
            digits,
            numbers,
        );
    }
}

fn write_to_file(filename: &str, lines: &[String]) -> Result<()> {
    let mut file = File::create(filename)?;

    for line in lines {
        writeln!(file, "{}", line)?; // Using writeln! for automatic newlines
    }

    Ok(())
}

fn main() {
    let length = 15;
    let result = generate_numbers(length);

    let filename = "output.txt";
    if let Err(e) = write_to_file(filename, &result) {
        eprintln!("Error writing to file: {}", e); // Using eprintln! for error output
        return;
    }

    println!("Numbers successfully saved to {}", filename);
}
