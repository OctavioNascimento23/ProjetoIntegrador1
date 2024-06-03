-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 03/06/2024 às 02:47
-- Versão do servidor: 10.4.25-MariaDB
-- Versão do PHP: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `projeto`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `produto`
--

CREATE TABLE `produto` (
  `idProduto` int(4) NOT NULL,
  `nomeProduto` varchar(50) NOT NULL,
  `descProduto` varchar(150) NOT NULL,
  `impostoProduto` float(4,2) NOT NULL,
  `custoAquisicao` float(7,2) NOT NULL,
  `custoFixo` float(4,2) NOT NULL,
  `comissaoVendas` float(4,2) NOT NULL,
  `rentabilidadeProduto` float(4,2) NOT NULL,
  `precoVenda` float(7,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Despejando dados para a tabela `produto`
--

INSERT INTO `produto` (`idProduto`, `nomeProduto`, `descProduto`, `impostoProduto`, `custoAquisicao`, `custoFixo`, `comissaoVendas`, `rentabilidadeProduto`, `precoVenda`) VALUES
(1, 'ProdutoTeste', 'ProdutoTeste_1', 10.00, 1500.00, 20.00, 1.00, 20.00, 3061.22),
(2, 'ProdutoTeste2', 'ProdutoTeste_2', 10.50, 99.99, 2.50, 2.00, 20.20, 154.31),
(3, 'PT3', 'PT3', 10.00, 150.00, 10.50, 1.50, 20.50, 260.87);

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `produto`
--
ALTER TABLE `produto`
  ADD PRIMARY KEY (`idProduto`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `produto`
--
ALTER TABLE `produto`
  MODIFY `idProduto` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
