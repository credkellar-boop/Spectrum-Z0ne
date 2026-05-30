use std::process::{Command, Stdio};

pub fn run_ar_dashboard() {
    println!("Initializing Spectrum-Z0ne AR Dashboard...");
    println!("Booting Companion App and Gemini AI Bridge services...");

    let mut child = Command::new("docker-compose")
        .arg("up")
        .arg("--build")
        .stdout(Stdio::inherit())
        .stderr(Stdio::inherit())
        .spawn()
        .expect("Failed to execute docker-compose. Is Docker installed and running?");

    let status = child.wait().expect("Failed to wait on docker-compose process");

    if status.success() {
        println!("Spectrum-Z0ne services shut down cleanly.");
    } else {
        eprintln!("Spectrum-Z0ne services exited with an error status: {}", status);
    }
}
