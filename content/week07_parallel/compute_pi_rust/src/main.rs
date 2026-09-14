// Based on Tim Mattson's code for https://github.com/tgmattso/OpenMP_intro_tutorial


fn main() {
    let num_steps = 100000000;
    let start = std::time::Instant::now();

    let step = 1.0/f64::try_from(num_steps).unwrap();

    let sum: f64 = (0..num_steps).map(|i| {
        let x = (f64::from(i)+0.5)*step;
        4.0/(1.0+x*x)
    }).sum();

    let pi = step * sum;
    let elapsed = start.elapsed();
    println!("π is {pi} in {elapsed:.2?}!");
}
