FROM alpine:3.20

# Tambah user non-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Install paket minimal & bersih
RUN apk add --no-cache curl bash

# Healthcheck untuk container
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost/ || exit 1

# Set user non-root
USER appuser

CMD ["bash"]
