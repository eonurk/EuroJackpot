# Shared visual identity for every chart on the Eurojackpot Analysis site.
# Sourced from each page's setup chunk so all figures read as one system.
#
# Color roles (validated for contrast + color-vision-deficiency separation):
#   main numbers  -> blue        euro numbers -> gold
#   2nd category  -> green       expected / theory reference -> neutral gray
#   outliers / thresholds -> red ordered series -> one blue ramp, light to dark

library(ggplot2)

ej_blue      <- "#2a78d6" # main numbers
ej_blue_dark <- "#1c5cab"
ej_blue_deep <- "#0d366b"
ej_blue_pale <- "#cde2fb"
ej_gold      <- "#c98500" # euro numbers
ej_gold_soft <- "#eda100"
ej_green     <- "#008300" # second categorical slot
ej_red       <- "#d03b3b" # outliers, chance thresholds
ej_ink       <- "#0b0b0b"
ej_ink2      <- "#52514e"
ej_muted     <- "#898781" # neutral reference ("expected under randomness")
ej_grid      <- "#e1e0d9"
ej_surface   <- "#fcfcfb"

# Ordered series (ball positions, rule eras, consecutive pairs) share one
# light-to-dark blue ramp instead of a rainbow
ej_ramp <- function(n) colorRampPalette(c("#86b6ef", "#0d366b"))(n)

ej_caption <- "Source: Eurojackpot official draws · github.com/eonurk/eurojackpot"

# Chart text uses the same sans as the site's data layer (tables, captions,
# labels). If Inter is not installed the graphics device silently falls back
# to the default sans, so rendering never breaks on another machine.
ej_font <- "Inter"

theme_ej <- function(base_size = 15, base_family = ej_font) {
    theme_minimal(base_size = base_size, base_family = base_family) +
        theme(
            text = element_text(color = ej_ink2),
            plot.title = element_text(
                color = ej_ink, face = "bold",
                size = rel(1.25), margin = margin(b = 6)
            ),
            plot.subtitle = element_text(
                color = ej_muted, size = rel(0.9), margin = margin(b = 14)
            ),
            plot.caption = element_text(
                color = ej_muted, size = rel(0.7), hjust = 0, margin = margin(t = 16)
            ),
            plot.title.position = "plot",
            plot.caption.position = "plot",
            axis.title = element_text(color = ej_ink2, size = rel(0.9)),
            axis.text = element_text(color = ej_muted, size = rel(0.85)),
            legend.position = "bottom",
            legend.title = element_blank(),
            legend.text = element_text(color = ej_ink2, size = rel(0.9)),
            panel.grid.minor = element_blank(),
            panel.grid.major = element_line(color = ej_grid, linewidth = 0.4),
            strip.text = element_text(color = ej_ink, face = "bold", size = rel(0.9)),
            plot.background = element_rect(fill = ej_surface, color = NA),
            panel.background = element_rect(fill = ej_surface, color = NA),
            plot.margin = margin(18, 18, 14, 18)
        )
}

theme_set(theme_ej())

# geom_text()/annotate("text") do not inherit the theme family - set it once
update_geom_defaults("text", list(family = ej_font))
