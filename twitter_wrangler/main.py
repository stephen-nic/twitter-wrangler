from omegaconf import DictConfig, OmegaConf
import hydra
import logging
from twitter_wrangler.utils.twitter_api import Twitter

log = logging.getLogger(__name__)


@hydra.main(config_path='conf', config_name='config')
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    twitter = Twitter(cfg)
    twitter.verify_credentials()


if __name__ == "__main__":
    my_app()
