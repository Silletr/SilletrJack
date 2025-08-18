return {
  "Silletr/LazyDeveloperHelper",
  config = function()
    require("plugins.LazyDeveloperHelper").setup()
  end
}

--[[
  FOR PACKER:
use {
  "Silletr/LazyDeveloperHelper",
  config = function()
    require("LazyDeveloperHelper").setup()
  end
}

  FOR vim-plug:
  Plug 'Silletr/LazyDeveloperHelper'
  lua require("LazyDeveloperHelper").setup()

  FOR LazyNvim:
  return {
  "Silletr/LazyDeveloperHelper",
  config = function()
    require("LazyDeveloperHelper").setup()
  end
}
  ]]
