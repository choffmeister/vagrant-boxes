#!/usr/bin/env bash
apt-get update

## ============================================
## Install Mono and NUnit
## ============================================

apt-get install -y mono-devel mono-gmcs
apt-get install -y nunit-console
