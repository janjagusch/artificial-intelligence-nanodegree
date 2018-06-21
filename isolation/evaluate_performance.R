require(magrittr)
require(reshape)

data <- "[233, 244, 234, 238]
[235, 245, 227, 243]
[247, 250, 237, 249]
[241, 262, 237, 234]
[216, 228, 236, 248]
[238, 244, 232, 241]
[233, 245, 222, 247]
[233, 254, 241, 241]
[239, 237, 237, 228]
[225, 239, 240, 238]
[232, 249, 232, 250]
[227, 249, 232, 240]
[233, 238, 227, 238]
[233, 256, 241, 250]
[230, 242, 222, 245]
[241, 224, 243, 249]
[246, 236, 243, 244]
[215, 239, 241, 225]
[235, 250, 237, 242]
[235, 236, 237, 246]
[242, 245, 236, 244]
[234, 257, 238, 235]
[232, 240, 220, 257]
[242, 244, 237, 248]
[246, 243, 231, 244]
[232, 262, 233, 238]
[237, 243, 232, 240]
[237, 253, 233, 246]
[238, 247, 235, 252]
[228, 240, 242, 249]"

data <- gsub("\\[|\\]| ", "", data) %>% strsplit(",|\n") %>% unlist() %>% as.numeric() %>% matrix(nrow = 30, byrow = T) %>% as.data.frame()
colnames(data) <- c("AB Improved", "AB Central", "AB Pressure", "AB Central Pressure")
data <- data * 100 / 350
data$id <- rownames(data)

plot.data <- melt.data.frame(data, id.vars = "id")
plot.data$id <- NULL

data$id <- NULL

require(ggplot2)
require(extrafont)
require(ggthemes)

# font_import(pattern="[C/c]ambria")
# loadfonts(device="win")

theme_set(theme_classic() + theme(text=element_text(size=8, family="Cambria")))

ggplot(data = plot.data, aes(x = variable, y= value)) +
  geom_boxplot() +
  labs(
    x = "Agent",
    y = "Wins %"
  )

ggsave("plot.pdf", width = 5, height = 3)

stat.data <- data

wilcox.test(stat.data$`AB Central`, stat.data$`AB Improved`, paired = F, exact = F, alternative = "greater")
wilcox.test(stat.data$`AB Pressure`, stat.data$`AB Improved`, paired = F, exact = F, alternative = "greater")
wilcox.test(stat.data$`AB Central Pressure`, stat.data$`AB Improved`, paired = F, exact = F, alternative = "greater")
