# Build script for Eurojackpot Analysis website

# Load required packages
if (!require("rmarkdown")) install.packages("rmarkdown")

# Build the website
rmarkdown::render_site()

# Print success message
cat("Website built successfully! Output is in the 'docs' directory.\n")
cat("To view the website locally, open 'docs/index.html' in your browser.\n")
