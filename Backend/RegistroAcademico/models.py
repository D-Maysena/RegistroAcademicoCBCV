from django.db import models


class Asignacionaula(models.Model):
    codigoaula = models.OneToOneField('Aula', on_delete=models.CASCADE, db_column='CodigoAula', primary_key=True)  # Field name made lowercase. The composite primary key (CodigoAula, CodigoGrupo, CodigoTurno) found, that is not supported. The first column is selected.
    codigogrupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, db_column='CodigoGrupo')  # Field name made lowercase.
    codigoturno = models.ForeignKey('Turno', on_delete=models.CASCADE, db_column='CodigoTurno')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'AsignacionAula'
        unique_together = (('codigoaula', 'codigogrupo', 'codigoturno'),)

    def __str__(self):
        return f"{self.codigoaula} asignada al grupo {self.codigogrupo} a las {self.codigoturno}"


class Asignaciondocente(models.Model):
    ceduladocente = models.OneToOneField('Docente',  on_delete=models.CASCADE, db_column='CedulaDocente', primary_key=True)  # Field name made lowercase. The composite primary key (CedulaDocente, CodigoGrupo) found, that is not supported. The first column is selected.
    codigogrupo = models.ForeignKey('Grupo',  on_delete=models.CASCADE, db_column='CodigoGrupo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AsignacionDocente'
        unique_together = (('ceduladocente', 'codigogrupo'),)
        
    def __str__(self):
        return f"{self.ceduladocente} asignado al grupo {self.codigogrupo}"


class Asignatura(models.Model):
    codigoasignatura = models.IntegerField(db_column='CodigoAsignatura', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    idasignatura = models.CharField(db_column='IdAsignatura', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Asignatura'

    def __str__(self):
        return f"{self.nombre} - {self.idasignatura}"

class Aula(models.Model):
    codigoaula = models.IntegerField(db_column='CodigoAula', primary_key=True)  # Field name made lowercase.
    capacidad = models.IntegerField(db_column='Capacidad')  # Field name made lowercase.
    numeroaula = models.IntegerField(db_column='NumeroAula')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Aula'

    def __str__(self):
        return f"Aula: {self.codigoaula} - Capacidad: {self.capacidad} - Naula: {self.numeroaula}"

class Docente(models.Model):
    ceduladocente = models.CharField(db_column='CedulaDocente', primary_key=True, max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    apellido = models.CharField(db_column='Apellido', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    especialidad = models.CharField(db_column='Especialidad', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Docente'

    def __str__(self):
        return f"Docente: {self.nombre} {self.apellido} - Especialidad: {self.especialidad}"

class Estudiante(models.Model):
    codestudiante = models.CharField(db_column='CodEstudiante', primary_key=True, max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre1 = models.CharField(db_column='Nombre1', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre2 = models.CharField(db_column='Nombre2', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    apellido1 = models.CharField(db_column='Apellido1', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    apellido2 = models.CharField(db_column='Apellido2', max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fechanac = models.CharField(db_column='FechaNac', max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    edad = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='Sexo', max_length=10, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cedulaalumno = models.CharField(db_column='CedulaAlumno', max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    direccionalumno = models.CharField(db_column='DireccionAlumno', max_length=100, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    codigogrupo = models.ForeignKey('Grupo', on_delete=models.CASCADE, db_column='CodigoGrupo', blank=True, null=True)  # Field name made lowercase.
    codigotutor = models.ForeignKey('Tutor', on_delete=models.CASCADE, db_column='CodigoTutor', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Estudiante'

    def __str__(self):
        return f"{self.nombre1} {self.nombre2} {self.apellido1} {self.apellido2} "



class Grupo(models.Model):
    codigogrupo = models.IntegerField(db_column='CodigoGrupo', primary_key=True)  # Field name made lowercase.
    nivelacademico = models.CharField(db_column='NivelAcademico', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Grupo'

    def __str__(self):
        return f"Grupo: {self.codigogrupo} {self.nombre} {self.nivelacademico}"

class Horario(models.Model):
    codigohorario = models.IntegerField(db_column='CodigoHorario', primary_key=True)  # Field name made lowercase.
    horainicio = models.TimeField(db_column='HoraInicio')  # Field name made lowercase.
    horafin = models.TimeField(db_column='HoraFin')  # Field name made lowercase.
    codigogrupo = models.ForeignKey(Grupo,on_delete=models.CASCADE, db_column='CodigoGrupo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Horario'

    def __str__(self):
        return f"Horario: Inicio {self.horainicio} - {self.horafin} - {self.codigogrupo}"


class Inscribe(models.Model):
    IdInscribe = models.AutoField(primary_key=True)  # AutoField es equivalente a un campo INT IDENTITY en SQL
    codestudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, db_column='CodEstudiante')
    codigoasignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, db_column='CodigoAsignatura')
    fechainscripcion = models.DateField(db_column='FechaInscripcion')

    class Meta:
        db_table = 'Inscribe'
        unique_together = (('codestudiante', 'codigoasignatura'),)

    def __str__(self):
        return f"Inscribe: {self.codestudiante} - {self.codigoasignatura} - Fecha {self.fechainscripcion}"

class Registronotas(models.Model):
    IdRegistro = models.AutoField(primary_key=True)  # Primary key with auto-increment    
    codestudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, db_column='CodEstudiante')
    codigoasignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, db_column='CodigoAsignatura')
    periodoacademico = models.CharField(db_column='PeriodoAcademico', max_length=20, db_collation='Modern_Spanish_CI_AS')
    parcial1 = models.DecimalField(db_column='Parcial1', max_digits=5, decimal_places=2, blank=True, null=True)
    parcial2 = models.DecimalField(db_column='Parcial2', max_digits=5, decimal_places=2, blank=True, null=True)
    parcial3 = models.DecimalField(db_column='Parcial3', max_digits=5, decimal_places=2, blank=True, null=True)
    parcial4 = models.DecimalField(db_column='Parcial4', max_digits=5, decimal_places=2, blank=True, null=True)
    notafinal = models.DecimalField(db_column='NotaFinal', max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'RegistroNotas'


    def __str__(self):
        return f"Registro Notas: {self.codestudiante} - {self.codigoasignatura}"


class Turno(models.Model):
    codigoturno = models.IntegerField(db_column='CodigoTurno', primary_key=True)  # Field name made lowercase.
    horario = models.CharField(db_column='Horario', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Turno'

    def __str__(self):
        return f"Turno: {self.horario}"


class Tutor(models.Model):
    codigotutor = models.IntegerField(db_column='CodigoTutor', primary_key=True)  # Field name made lowercase.
    nombretutor = models.CharField(db_column='NombreTutor', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cedulatutor = models.CharField(db_column='CedulaTutor', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tutor'
        
    def __str__(self):
        return f"Tutor: {self.nombretutor} - {self.cedulatutor}"