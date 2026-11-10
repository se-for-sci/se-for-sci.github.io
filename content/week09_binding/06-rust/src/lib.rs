use pyo3::prelude::*;

#[pymodule]
mod rust_example {
    use pyo3::prelude::*;

    #[pyfunction]
    fn square(a: usize) -> usize {
        a * a
    }
}
