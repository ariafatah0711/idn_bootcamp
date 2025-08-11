# Gunakan base image Alpine versi terbaru yang ringan
FROM alpine:3.20

# Set environment agar build reproducible dan lebih aman
ENV USERNAME=appuser

# Install bash dengan versi terbaru dan hapus cache agar image tetap kecil
RUN apk add --no-cache bash \
    && addgroup -S $USERNAME \
    && adduser -S $USERNAME -G $USERNAME

# Beralih ke user non-root
USER $USERNAME

# Gunakan shell script atau command default
CMD ["bash"]