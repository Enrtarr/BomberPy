import ursina as urs

if __name__ == '__main__':
    app = urs.Ursina()


class Bomb(urs.Entity):
    def __init__(self, murs_incassables:urs.Entity, murs_cassables:urs.Entity, bombes:urs.Entity, balles:urs.Entity, **kwargs): 
        super().__init__()
        """Initialisation de la bombe et de ses attributs
            - rotation_x : permet de faire en sorte que la bombe fasse face à la caméra
            - scale : la déformation de la bombe
            - __tex_folder : le dossier contenant les textures de la bombe (et de l'explosion)
            - longueur : la longeur des branches de la bombe
            - murs_incassables : une entité utilisée pour le raycasting des branches
            - murs_cassables : une entité utilisée pour le raycasting des branches
            - bombes : une entité utilisée pour une organisation plus propre des branches
            - __anims : les animations de la bombe
        """

        self.rotation_x = -90
        self.scale=1
        self.__tex_folder = './textures/explosion/'
        self.longueur = 3
        
        self.murs_incassables = murs_incassables
        self.murs_cassables = murs_cassables
        self.bombes = bombes
        self.balles = balles

        self.__anims = urs.SpriteSheetAnimation(
            texture='./textures/bomb_flash.png',
            tileset_size=(6,1),
            fps=6,
            model='plane',
            animations={
                'flash': ((0,0), (5,0)),
            }
        )
        self.__anims.parent = self
        self.__anims.play_animation('flash')
        
        for key, value in kwargs.items(): 
            setattr(self, key, value)
    
    def explode(self):
        """Méthode appelée afin de faire exploser la bombe
        Elle va simplement créer les durées entre les animation ainsi que les entités parentes pour chacune des branches, 
        puis appelera la méthode branche() pour chacune des quatres directions cardinales. Enfin, elle se désactivera  (puisque le module
        Ursina est bogué). Les branches quand à elles se suppriment seules à la fin de l'explosion.
        """
        # les différentes durées entres les animations
        duration = .3
        wt1 = duration/3
        wt2 = 2 * duration/3
        wt3 = duration
        wt4 = duration + duration/3
        
        # créeation, animation et destruction du cube central
        m1 = urs.Entity(scale=self.scale,model='quad',position=self.position,collider='box') ; m1.texture = self.__tex_folder + 'm11'
        urs.invoke(setattr, m1, 'texture', self.__tex_folder+'m21', delay=wt1)
        urs.invoke(setattr, m1, 'texture', self.__tex_folder+'m31', delay=wt2)
        urs.invoke(setattr, m1, 'texture', self.__tex_folder+'m41', delay=wt3)
        urs.destroy(m1, delay=wt4)
        
        # on créer des parents pour chaque branche
        bombe_d = urs.Entity(model='quad', texture='./textures/vide',position=self.position)
        bombe_g = urs.Entity(model='quad', texture='./textures/vide',position=self.position)
        bombe_h = urs.Entity(model='quad', texture='./textures/vide',position=self.position)
        bombe_b = urs.Entity(model='quad', texture='./textures/vide',position=self.position)
        
        # on appelle la création des quatres branches
        self.branche(bombe_d,'d',wt1,wt2,wt3,wt4,self.murs_incassables,self.murs_cassables,self.balles,1,0)
        self.branche(bombe_g,'g',wt1,wt2,wt3,wt4,self.murs_incassables,self.murs_cassables,self.balles,-1,0)
        self.branche(bombe_h,'h',wt1,wt2,wt3,wt4,self.murs_incassables,self.murs_cassables,self.balles,0,1)
        self.branche(bombe_b,'b',wt1,wt2,wt3,wt4,self.murs_incassables,self.murs_cassables,self.balles,0,-1)
        
        # on change le parent pour le milieu et chaque branche
        m1.parent = self.bombes
        bombe_d.parent = self.bombes
        bombe_g.parent = self.bombes
        bombe_h.parent = self.bombes
        bombe_b.parent = self.bombes

        # on supprime les bombes (cause du bug, à modifier)
        for i in urs.scene.entities:
            if type(i) == urs.SpriteSheetAnimation:
                if 'flash' in i.animations and (i.parent == self):
                    i.disable()
    
    # fonction pour chaque branche de l'explosion
    def branche(
        self,
        b_cote:urs.Entity, cote:str,
        wt1:float, wt2:float, wt3:float, wt4:float,
        murs_incassables:urs.Entity, murs_cassables:urs.Entity, balles:urs.Entity,
        x_offset:int, y_offset:int,
        ):
        """Méthode permettant de créer une branche dans une des quatres directions cardinales
            - b_cote : l'entité qui sera parente des "tiles" de la branche
            - cote : le nom du cote, utilisé pour l'application des textures
            - wt1, wt2, wt3, wt4 : le temps entre chaque "frame" des animations
            - murs_incassables : une entité utilisée pour le raycasting des branches
            - murs_cassables : une entité utilisée pour le raycasting des branches
            - balles : une entité utilisée pour le raycasting des balles
            - x_offset, y_offset : determine la direction prise par la branche
                (droite=(1,0) ; gauche=(-1,0) ; haut=(0,1) ; bas=(0,-1))
        """
        for i in range(self.longueur):
            # raycast pour les deux types de mur
            hit_UnWall = urs.raycast(b_cote.position, (x_offset,y_offset), traverse_target=murs_incassables, distance=i+1, debug=False)
            hit_BrWall = urs.raycast(b_cote.position, (x_offset,y_offset), traverse_target=murs_cassables, distance=i+1, debug=False)
            # mur incassable : on stoppe le rayon
            if hit_UnWall:
                break
            # mur cassable : on le casse et on créer un bout, puis on stoppe le rayon
            elif hit_BrWall:
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=b_cote)
                new_sprite.x += x_offset*(i+1)
                new_sprite.y += y_offset*(i+1)
                new_sprite.texture = self.__tex_folder+cote+'12'
                new_sprite.name = 'bout'
                urs.destroy(hit_BrWall.entity)
                break
            # si aucun mur :
            else:
                # on créer un nouveau bout
                new_sprite = urs.Entity(scale=self.scale,model='quad',collider='box',parent=b_cote)
                new_sprite.x += x_offset*(i+1)
                new_sprite.y += y_offset*(i+1)
                new_sprite.texture = self.__tex_folder+cote+'11'
                # si on est à la fin de la branche, on transforme le cube en bout
                if i+1 == self.longueur:
                    new_sprite.texture = self.__tex_folder+cote+'12'
                    new_sprite.name = 'bout'
                # on regarde si on touche une balle
                hit_Ball = urs.boxcast(b_cote.position, (x_offset,y_offset), traverse_target=balles,thickness=(1,1) , distance=i+1)
                # si on en touche une :
                if hit_Ball:
                    # on la décale jusqu'au bout de la branche actuelle (qui n'est pas forcément finie)
                    # hit_Ball.entity.x += x_offset*(self.longueur-i)
                    # hit_Ball.entity.y += y_offset*(self.longueur-i)
                    hit_Ball.entity.x_velocity += x_offset*(self.longueur-i)
                    hit_Ball.entity.y_velocity += y_offset*(self.longueur-i)
        # mise à jour des textures au fil du temps :
        for sprite in b_cote.children:
            # si ce n'est pas un bout
            if sprite.name != 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+cote+'21', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+cote+'31', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+cote+'41', delay=wt3)
                urs.destroy(sprite, delay=wt4)
            # si c'est un bout
            elif sprite.name == 'bout':
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+cote+'22', delay=wt1)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+cote+'32', delay=wt2)
                urs.invoke(setattr, sprite, 'texture', self.__tex_folder+cote+'42', delay=wt3)
                urs.destroy(sprite, delay=wt4)

if __name__ == '__main__':
    app.run()