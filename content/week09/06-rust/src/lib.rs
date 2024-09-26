use pyo3::prelude::*;

#[pymodule]
mod rust_example {
    use super::*;

  #[pyfunction]
  fn square(a: usize, b: usize) -> usize {
      a + b
  }
}
